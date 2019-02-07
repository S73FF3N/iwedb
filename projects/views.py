from datetime import datetime
from calendar import mdays
import itertools
from django_tables2 import MultiTableMixin, SingleTableMixin
from django_tables2.config import RequestConfig
from django_filters.views import FilterView
from weasyprint import HTML
import tempfile
from django.http import JsonResponse

from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from django.db.models import Min, Case, When

from .models import Project, Comment, Calculation_Tool
from .tables import ProjectTable, TotalVolumeTable, NewEntriesTable, Calculation_ToolTable
from .filters import ProjectListFilter, Calculation_ToolFilter
from .utils import PagedFilteredTableView
from .forms import ProjectForm, CommentForm, DrivingForm, ContractsInCloseDistanceForm
from turbine.forms import ContractForm

class ProjectList(PagedFilteredTableView):
    model = Project
    table_class = ProjectTable
    filter_class = ProjectListFilter

class ProjectCreate(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "projects/project_form.html"
    model = Project
    form_class = ProjectForm
    permission_required = 'projects.has_sales_status'
    raise_exception = True

    def form_valid(self, form):
        form.instance.available = True
        form.instance.slug = orig = slugify(str(form.instance.name))
        for x in itertools.count(1):
            if not Project.objects.filter(slug=form.instance.slug).exists():
                break
            form.instance.slug = '%s-%d' % (orig, x)

        form.instance.created = datetime.now()
        form.instance.updated = datetime.now()
        if form.instance.status in ['Cancelled', 'Lost']:
            form.instance.prob = 0
        elif form.instance.status == 'Won':
            form.instance.prob = 100
        redirect = super(ProjectCreate, self).form_valid(form)
        project_created = self.object
        #today = date.today()
        #year = today.year
        #self.object.offer_nr = "".join(("A", str(year), str(project_created.pk)))
        #self.object.save()
        comment = Comment(text='created project', object_id=project_created.id, content_type=ContentType.objects.get(app_label = 'projects', model = 'project'), created=datetime.now(), created_by=self.request.user)
        comment.save()
        return redirect

class ProjectEdit(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    permission_required = 'projects.has_sales_status'
    raise_exception = True

    def form_valid(self, form):
        form.instance.available = True
        form.instance.updated = datetime.now()
        if form.instance.status in ['Cancelled', 'Lost']:
            form.instance.prob = 0
        elif form.instance.status == 'Won':
            form.instance.prob = 100
        comment = Comment(text='edited project', object_id=self.kwargs['pk'], content_type=ContentType.objects.get(app_label = 'projects', model = 'project'), created=datetime.now(), created_by=self.request.user)
        comment.save()
        return super(ProjectEdit, self).form_valid(form)

def validate_project_name(request):
    project_name = request.POST.get('project_name')
    data = {
        'is_taken': Project.objects.filter(name__iexact=project_name, available=True).exists(),
        'similar_projects': list(Project.objects.filter(name__icontains=project_name, available=True).values('name', 'status', 'customer__name'))
        }
    return JsonResponse(data)

class CommentCreate(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Comment
    form_class = CommentForm
    permission_required = 'projects.has_sales_status'
    raise_exception = True

    def get_success_url(self):
        project = get_object_or_404(Project, id=self.kwargs['project_id'])
        success_url = reverse_lazy('projects:project_detail', kwargs={'id': project.id, 'slug': project.slug})
        return success_url

    def form_valid(self, form):
        form.instance.available = True
        form.instance.object_id = self.kwargs['project_id']
        form.instance.content_type = ContentType.objects.get(app_label = 'projects', model = 'project')
        form.instance.created = datetime.now()
        form.instance.created_by = self.request.user
        return super(CommentCreate, self).form_valid(form)

class CommentEdit(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    permission_required = 'projects.has_sales_status'
    raise_exception = True

    def get_success_url(self):
        project = get_object_or_404(Project, id=self.kwargs['project_id'])
        success_url = reverse_lazy('projects:project_detail', kwargs={'id': project.id, 'slug': project.slug})
        return success_url

    def form_valid(self, form):
        form.instance.available = True
        form.instance.object_id = self.kwargs['project_id']
        form.instance.content_type = ContentType.objects.get(app_label = 'projects', model = 'project')
        return super(CommentEdit, self).form_valid(form)

def project_detail(request, id, slug):
    project = get_object_or_404(Project, id=id, slug=slug)
    comments = project.comment.all().exclude(text__in=["created project", "edited project"])
    changes = project.comment.all().filter(text__in=["created project", "edited project"])
    result = None
    surrounding_contracts = None
    if request.method == "POST" and 'driving_form' in request.POST:
        contracts_in_distance_form = ContractsInCloseDistanceForm(prefix="contracts_in_distance_form")
        driving_form = DrivingForm(request.POST, prefix="driving_costs_form")
        if driving_form.is_valid():
            distance = driving_form.cleaned_data["distance"]
            hours = driving_form.cleaned_data["hours"]
            result = project.driving_rate(distance, hours)
    if request.method == "POST" and 'surrounding_contracts_form' in request.POST:
        driving_form = DrivingForm(prefix="driving_costs_form")
        contracts_in_distance_form = ContractsInCloseDistanceForm(request.POST, prefix="contracts_in_distance_form")
        if contracts_in_distance_form.is_valid():
            distance = contracts_in_distance_form.cleaned_data["distance"]
            surrounding_contracts = project.contracts_in_100km_distance(distance)
    else:
        driving_form = DrivingForm(prefix="driving_costs_form")
        contracts_in_distance_form = ContractsInCloseDistanceForm(prefix="contracts_in_distance_form")

    return render(request, 'projects/detail.html', {'project': project, 'comments': comments, 'changes': changes, 'form': driving_form, 'contracts_in_distance_form': contracts_in_distance_form, 'result': result, 'surrounding_contracts': surrounding_contracts})

def project_to_contract(request, id, slug):
    project = get_object_or_404(Project, id=id, slug=slug)
    turbines = project.turbines.all()
    if project.price:
        price = project.price
    else:
        price = 0
    if project.start_operation:
        start = project.start_operation
    else:
        start = datetime.now()
    form = ContractForm(request.POST or None, request.FILES or None, initial={'turbines': turbines, 'start_date':start, 'average_remuneration':price})
    form.instance.active = True
    form.instance.created = datetime.now()
    form.instance.updated = datetime.now()
    if request.method == "POST":
        if form.is_valid():
            contract = form.save()
            comment = Comment(text='created contract', object_id=contract.id, content_type=ContentType.objects.get(app_label = 'turbine', model = 'contract'), created=datetime.now(), created_by=request.user)
            comment.save()
            return HttpResponseRedirect(reverse_lazy('turbines:contract_detail', kwargs={'id': contract.id}))
    return render(request, 'turbine/contract_form.html', {'form':form})

class Calculation_ToolList(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Calculation_Tool
    table_class = Calculation_ToolTable
    filterset_class = Calculation_ToolFilter
    template_name = 'projects/calculation_tool.html'

class TotalVolumeReport(LoginRequiredMixin, MultiTableMixin, FilterView):
    model = Project
    filterset_class = ProjectListFilter
    template_name = 'projects/reports/total_volume.html'

    def get_queryset(self,*args, **kwargs):
        qs = super(FilterView, self).get_queryset().filter(available=True).prefetch_related('turbines', 'turbines__wind_farm', 'turbines__wec_typ', 'turbines__wec_typ__manufacturer', 'turbines__wind_farm__country', 'turbines__owner', 'comment').select_related('customer', 'sales_manager').annotate(first_com_date=Case(When(turbines__commisioning__isnull=False, then=Min('turbines__commisioning')))).add_mw()
        self.filter = self.filterset_class(self.request.GET, queryset=qs)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super(MultiTableMixin, self).get_context_data(**kwargs)
        dates = {'first_of_year': datetime(year=datetime.today().year, month=1, day=1).strftime("%Y-%m-%d"), 'last_of_year':datetime(year=datetime.today().year, month=12, day=31).strftime("%Y-%m-%d"), 'first_of_month': datetime(year=datetime.today().year, month=datetime.today().month, day=1).strftime("%Y-%m-%d"), 'last_of_month': datetime(year=datetime.today().year, month=datetime.today().month, day=mdays[datetime.today().month]).strftime("%Y-%m-%d"), 'today': datetime.today().strftime("%Y-%m-%d")}
        context["first_of_year"] = dates["first_of_year"]
        context["last_of_year"] = dates["last_of_year"]
        context["first_of_month"] = dates["first_of_month"]
        context["last_of_month"] = dates["last_of_month"]
        context["today"] = dates["today"]
        tables = [
            TotalVolumeTable(self.filter.qs.filter(status='Won', start_operation__range=[dates['first_of_year'], dates['last_of_year']])),
            TotalVolumeTable(self.filter.qs.filter(status__in=['Hard Offer', 'Negotiation', 'Final Negotiation'], prob__range=[90, 100], start_operation__range=[dates['first_of_month'], dates['last_of_month']])),
            NewEntriesTable(self.filter.qs.filter(request_date__range=[dates['first_of_month'], dates['today']]))
                ]
        table_counter = itertools.count()
        for table in tables:
            table.prefix = table.prefix or self.table_prefix.format(next(table_counter))
            RequestConfig(self.request, paginate=self.get_table_pagination(table)).configure(table)
            context[self.get_context_table_name(table)] = list(tables)
        return context

def create_pdf_scada_information(request, id, slug):
    project = get_object_or_404(Project, id=id, slug=slug)

    html_string = render_to_string('projects/reports/scada_information.html', {'project': project,})
    result = HTML(string=html_string).write_pdf()

    response = HttpResponse(result, content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename='+project.name+'_Laufzettel.pdf'
    return response
