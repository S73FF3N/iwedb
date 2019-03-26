from datetime import datetime, date
from calendar import mdays
import itertools
from django_tables2 import MultiTableMixin, SingleTableMixin
from django_tables2.config import RequestConfig
from django_filters.views import FilterView
from weasyprint import HTML
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
from django.forms.models import model_to_dict

from .models import Project, Comment, Calculation_Tool, OfferNumber, Reminder
from .tables import ProjectTable, TotalVolumeTable, NewEntriesTable, Calculation_ToolTable, OfferNumberTable
from .filters import ProjectListFilter, Calculation_ToolFilter, OfferNumberFilter
from .utils import PagedFilteredTableView
from .forms import ProjectForm, CommentForm, DrivingForm, ContractsInCloseDistanceForm, OfferNumberForm, TurbinesInCloseDistanceForm, ReminderForm
from turbine.forms import ContractForm

class ProjectList(PagedFilteredTableView):
    model = Project
    table_class = ProjectTable
    filter_class = ProjectListFilter

class ProjectCreate(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "projects/project_form.html"
    model = Project
    form_class = ProjectForm
    permission_required = 'projects.add_project'
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
        comment = Comment(text='created project', object_id=project_created.id, content_type=ContentType.objects.get(app_label = 'projects', model = 'project'), created=datetime.now(), created_by=self.request.user)
        comment.save()
        return redirect

class ProjectEdit(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    permission_required = 'projects.change_project'
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

def get_contracts_in_distance(request):
    distance = request.POST.get('distance')
    project_id = request.POST.get('project')
    project = Project.objects.get(id=project_id)
    data = {
        'contracts': project.contracts_in_100km_distance(distance)
        }
    return JsonResponse(data)

def get_turbines_in_distance(request):
    distance = request.POST.get('distance')
    manufacturer = request.POST.get('manufacturer')
    project_id = request.POST.get('project')
    project = Project.objects.get(id=project_id)
    data = {
        'turbines': project.turbines_in_distance(manufacturer, distance)
        }
    return JsonResponse(data)

def calculate_driving_rate(request):
    distance = request.POST.get('distance')
    minutes = request.POST.get('minutes')
    project_id = request.POST.get('project')
    project = Project.objects.get(id=project_id)
    data = {
        'driving_rates': project.driving_rate(distance, minutes)
        }
    return JsonResponse(data)

class CommentCreate(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Comment
    form_class = CommentForm
    permission_required = 'projects.can_comment_projects'
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
    permission_required = 'projects.can_comment_projects'
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

class ReminderCreate(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Reminder
    form_class = ReminderForm
    permission_required = 'projects.can_set_reminders'
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
        return super(ReminderCreate, self).form_valid(form)

def project_detail(request, id, slug):
    project = get_object_or_404(Project, id=id, slug=slug)
    comments = project.comment.exclude(text__in=["created project", "edited project"])
    changes = project.comment.filter(text__in=["created project", "edited project"])
    reminder = project.reminder.filter(date__gte=datetime.today())
    if request.method == "POST" and 'driving_form' in request.POST:
        contracts_in_distance_form = ContractsInCloseDistanceForm(prefix="contracts_in_distance_form")
        driving_form = DrivingForm(request.POST, prefix="driving_costs_form")
        awarding_form = ProjectForm(prefix="awarding_form")
        turbines_in_distance_form = TurbinesInCloseDistanceForm(prefix="turbines_in_distance_form")
    elif request.method == "POST" and 'surrounding_contracts_form' in request.POST:
        driving_form = DrivingForm(prefix="driving_costs_form")
        contracts_in_distance_form = ContractsInCloseDistanceForm(request.POST, prefix="contracts_in_distance_form")
        awarding_form = ProjectForm(prefix="awarding_form")
        turbines_in_distance_form = TurbinesInCloseDistanceForm(prefix="turbines_in_distance_form")
    elif request.method == "POST" and 'awarding_reason_form' in request.POST:
        driving_form = DrivingForm(prefix="driving_costs_form")
        contracts_in_distance_form = ContractsInCloseDistanceForm(prefix="contracts_in_distance_form")
        awarding_form = ProjectForm(request.POST, prefix="awarding_form")
        turbines_in_distance_form = TurbinesInCloseDistanceForm(prefix="turbines_in_distance_form")
    elif request.method == "POST" and 'surrounding_turbines_form' in request.POST:
        driving_form = DrivingForm(prefix="driving_costs_form")
        contracts_in_distance_form = ContractsInCloseDistanceForm(prefix="contracts_in_distance_form")
        awarding_form = ProjectForm(prefix="awarding_form")
        turbines_in_distance_form = TurbinesInCloseDistanceForm(request.POST, prefix="turbines_in_distance_form")
    else:
        driving_form = DrivingForm(prefix="driving_costs_form")
        contracts_in_distance_form = ContractsInCloseDistanceForm(prefix="contracts_in_distance_form")
        awarding_form = ProjectForm(prefix="awarding_form")
        turbines_in_distance_form = TurbinesInCloseDistanceForm(prefix="turbines_in_distance_form")

    return render(request, 'projects/detail.html', {'project': project, 'comments': comments, 'changes': changes, 'form': driving_form, 'contracts_in_distance_form': contracts_in_distance_form, 'turbines_in_distance_form': turbines_in_distance_form, 'awarding_form': awarding_form, 'reminder': reminder})

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
    if project.run_time:
        end_day = start.day
        end_month = start.month
        end_year = start.year + project.run_time
        end = date(end_year, end_month, end_day)
    else:
        end = datetime.now()
    form = ContractForm(request.POST or None, request.FILES or None, initial={'turbines': turbines, 'start_date':start, 'end_date':end, 'average_remuneration':price})
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
        qs = super(TotalVolumeReport, self).get_queryset().filter(available=True).prefetch_related('turbines', 'turbines__wind_farm', 'turbines__wec_typ', 'turbines__wec_typ__manufacturer', 'turbines__wind_farm__country', 'turbines__owner', 'comment').select_related('customer', 'sales_manager').annotate(first_com_date=Case(When(turbines__commisioning_year__isnull=False, then=Min('turbines__commisioning_year')))).add_mw()
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


class OfferNumberList(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = OfferNumber
    table_class = OfferNumberTable
    filterset_class = OfferNumberFilter
    template_name = "projects/offer_number_list.html"

class OfferNumberCreate(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "projects/offer_number_form.html"
    model = OfferNumber
    form_class = OfferNumberForm
    permission_required = 'projects.add_offernumber'
    raise_exception = True

    def get_initial(self, *args, **kwargs):
        initial = super(OfferNumberCreate, self).get_initial(**kwargs)
        today = datetime.now()
        year = today.year
        if OfferNumber.objects.latest().number[5] == "0":
            if OfferNumber.objects.latest().number[6] == "0":
                if OfferNumber.objects.latest().number[7] == "0":
                    new_offer_number = int(OfferNumber.objects.latest().number[8:])+1
                else:
                    new_offer_number = int(OfferNumber.objects.latest().number[7:])+1
            else:
                new_offer_number = int(OfferNumber.objects.latest().number[6:])+1
        elif OfferNumber.objects.latest().number[5:] == "9999":
            new_offer_number = 0
        else:
            new_offer_number = int(OfferNumber.objects.latest().number[5:])+1
        complete_number = "".join(("A", str(year), str(new_offer_number).zfill(4)))
        while complete_number in OfferNumber.objects.all().values_list('number', flat=True):
            complete_number = "".join(("A", str(year), str(new_offer_number+1).zfill(4)))
        initial['number'] = complete_number
        return initial

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.created = datetime.now()
        return super(OfferNumberCreate, self).form_valid(form)

def generate_offer_number(request):
    today = datetime.now()
    year = today.year
    if OfferNumber.objects.latest().number[5] == "0":
        if OfferNumber.objects.latest().number[6] == "0":
            if OfferNumber.objects.latest().number[7] == "0":
                new_offer_number = int(OfferNumber.objects.latest().number[8:])+1
            else:
                new_offer_number = int(OfferNumber.objects.latest().number[7:])+1
        else:
            new_offer_number = int(OfferNumber.objects.latest().number[6:])+1
    elif OfferNumber.objects.latest().number[5:] == "9999":
        new_offer_number = 0
    else:
        new_offer_number = int(OfferNumber.objects.latest().number[5:])+1
    complete_number = "".join(("A", str(year), str(new_offer_number).zfill(4)))
    while complete_number in OfferNumber.objects.all().values_list('number', flat=True):
        complete_number = "".join(("A", str(year), str(new_offer_number+1).zfill(4)))

    new_offer_number = OfferNumber.objects.create(number=complete_number, created_by=request.user, created=datetime.now())
    data = {
        'new_offer_number': model_to_dict(new_offer_number)}
    return JsonResponse(data)
