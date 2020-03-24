from datetime import datetime, date
from calendar import mdays
import itertools
from django_tables2 import MultiTableMixin, SingleTableMixin
from django_tables2.config import RequestConfig
from django_filters.views import FilterView
from weasyprint import HTML
import xlwt
#import logging

from django.http import JsonResponse
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import render, get_object_or_404
from django.utils.text import slugify
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from django.db.models import Min, Case, When
from django.forms.models import model_to_dict
from django.core.paginator import Paginator
from django.utils.translation import ugettext as _
from django.utils import translation

from .models import Project, Comment, Calculation_Tool, OfferNumber, Reminder, PoolProject, Document
from turbine.models import Turbine
from .tables import ProjectTable, TotalVolumeTable, NewEntriesTable, Calculation_ToolTable, OfferNumberTable, PoolProjectTable, DocumentTable
from .filters import ProjectListFilter, Calculation_ToolFilter, OfferNumberFilter, PoolProjectFilter
from .utils import PagedFilteredTableView, PoolTableView
from .forms import ProjectForm, CommentForm, DrivingForm, ContractsInCloseDistanceForm, OfferNumberForm, TurbinesInCloseDistanceForm, ReminderForm, PoolProjectForm
from turbine.forms import ContractForm
from events.models import Event, Date, translation_dict
from events.tables import DateTable

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

    def get_context_data(self, **kwargs):
        ctx = super(ProjectCreate, self).get_context_data(**kwargs)
        ctx['offer_number_form'] = OfferNumberForm
        return ctx

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
        if self.request.LANGUAGE_CODE == "en":
            with translation.override("de"):
                time_interval_en = 'days'
                time_interval_de = _(time_interval_en)
                duration_en = 'days'
                duration_de = _(duration_en)
                status_en = 'remaining'
                status_de = _(status_en)
                part_of_contract_en = 'yes'
                part_of_contract_de = _(part_of_contract_en)
                comment_en = 'Before contract commencement'
                comment_de = _(comment_en)
        else:
            time_interval_de = _('days')
            time_interval_en = translation_dict[str(time_interval_de)]
            duration_de = _('days')
            duration_en = translation_dict[str(duration_de)]
            status_de = _('remaining')
            status_en = translation_dict[str(status_de)]
            part_of_contract_de = _('yes')
            part_of_contract_en = translation_dict[str(part_of_contract_de)]
            comment_de = _('Before contract commencement')
            comment_en = translation_dict[str(comment_de)]
        if form.instance.zop == True:
            if self.request.LANGUAGE_CODE == "en":
                with translation.override("de"):
                    title_en = 'Condition based inspection'
                    title_de = _(title_en)
            else:
                title_de = _('Condition based inspection')
                title_en = translation_dict[str(title_de)]
            event = Event(title_de=title_de, title_en=title_en, every_count=1, time_interval_en=time_interval_en, time_interval_de=time_interval_de, for_count=0, duration_en=duration_en, duration_de=duration_de,done=date.today(), project=project_created)
            event.save()
            event.responsibles.add(self.request.user)
            for t in form.instance.turbines.all():
                event.turbines.add(t)
                first_date = Date(event=event, turbine=t, date=event.done, status_en=status_en, status_de=status_de, part_of_contract_en=part_of_contract_en, part_of_contract_de=part_of_contract_de, comment_en=comment_en, comment_de=comment_de)
                first_date.save()
        if form.instance.rotor == True:
            if self.request.LANGUAGE_CODE == "en":
                with translation.override("de"):
                    title_en = 'Rotor blade inspection'
                    title_de = _(title_en)
            else:
                title_de = _('Rotor blade inspection')
                title_en = translation_dict[str(title_de)]
            event = Event(title_de=title_de, title_en=title_en, every_count=1, time_interval_en=time_interval_en, time_interval_de=time_interval_de, for_count=0, duration_en=duration_en, duration_de=duration_de,done=date.today(), project=project_created)
            event.save()
            event.responsibles.add(self.request.user)
            for t in form.instance.turbines.all():
                event.turbines.add(t)
                first_date = Date(event=event, turbine=t, date=event.done, status_en=status_en, status_de=status_de, part_of_contract_en=part_of_contract_en, part_of_contract_de=part_of_contract_de, comment_en=comment_en, comment_de=comment_de)
                first_date.save()
        if form.instance.gearbox_endoscopy == True:
            if self.request.LANGUAGE_CODE == "en":
                with translation.override("de"):
                    title_en = 'Gearbox endoscopic inspection'
                    title_de = _(title_en)
            else:
                title_de = _('Gearbox endoscopic inspection')
                title_en = translation_dict[str(title_de)]
            event = Event(title_de=title_de, title_en=title_en, every_count=1, time_interval_en=time_interval_en, time_interval_de=time_interval_de, for_count=0, duration_en=duration_en, duration_de=duration_de,done=date.today(), project=project_created)
            event.save()
            event.responsibles.add(self.request.user)
            for t in form.instance.turbines.all():
                event.turbines.add(t)
                first_date = Date(event=event, turbine=t, date=event.done, status_en=status_en, status_de=status_de, part_of_contract_en=part_of_contract_en, part_of_contract_de=part_of_contract_de, comment_en=comment_en, comment_de=comment_de)
                first_date.save()
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
        if self.request.LANGUAGE_CODE == "en":
            with translation.override("de"):
                time_interval_en = 'days'
                time_interval_de = _(time_interval_en)
                duration_en = 'days'
                duration_de = _(duration_en)
                status_en = 'remaining'
                status_de = _(status_en)
                #part_of_contract_en = 'yes'
                #part_of_contract_de = _(part_of_contract_en)
                comment_en = 'Before contract commencement'
                comment_de = _(comment_en)
        else:
            time_interval_de = _('days')
            time_interval_en = translation_dict[str(time_interval_de)]
            duration_de = _('days')
            duration_en = translation_dict[str(duration_de)]
            status_de = _('remaining')
            status_en = translation_dict[str(status_de)]
            #part_of_contract_de = _('yes')
            #part_of_contract_en = translation_dict[str(part_of_contract_de)]
            comment_de = _('Before contract commencement')
            comment_en = translation_dict[str(comment_de)]
        if form.instance.zop == True:
            if self.request.LANGUAGE_CODE == "en":
                with translation.override("de"):
                    title_en = 'Condition based inspection'
                    title_de = _(title_en)
            else:
                title_de = _('Condition based inspection')
                title_en = translation_dict[str(title_de)]
            event = Event(title_de=title_de, title_en=title_en, every_count=1, time_interval_en=time_interval_en, time_interval_de=time_interval_de, for_count=0, duration_en=duration_en, duration_de=duration_de,done=date.today(), project=Project.objects.get(id=self.kwargs['pk']))
            event.save()
            event.responsibles.add(self.request.user)
            for t in form.instance.turbines.all():
                event.turbines.add(t)
                first_date = Date(event=event, turbine=t, date=event.done, status_en=status_en, status_de=status_de, comment_en=comment_en, comment_de=comment_de)
                first_date.save()
        if form.instance.rotor == True:
            if self.request.LANGUAGE_CODE == "en":
                with translation.override("de"):
                    title_en = 'Rotor blade inspection'
                    title_de = _(title_en)
            else:
                title_de = _('Rotor blade inspection')
                title_en = translation_dict[str(title_de)]
            event = Event(title_de=title_de, title_en=title_en, every_count=1, time_interval_en=time_interval_en, time_interval_de=time_interval_de, for_count=0, duration_en=duration_en, duration_de=duration_de,done=date.today(), project=Project.objects.get(id=self.kwargs['pk']))
            event.save()
            event.responsibles.add(self.request.user)
            for t in form.instance.turbines.all():
                event.turbines.add(t)
                first_date = Date(event=event, turbine=t, date=event.done, status_en=status_en, status_de=status_de, part_of_contract_en=part_of_contract_en, part_of_contract_de=part_of_contract_de, comment_en=comment_en, comment_de=comment_de)
                first_date.save()
        if form.instance.gearbox_endoscopy == True:
            if self.request.LANGUAGE_CODE == "en":
                with translation.override("de"):
                    title_en = 'Gearbox endoscopic inspection'
                    title_de = _(title_en)
            else:
                title_de = _('Gearbox endoscopic inspection')
                title_en = translation_dict[str(title_de)]
            event = Event(title_de=title_de, title_en=title_en, every_count=1, time_interval_en=time_interval_en, time_interval_de=time_interval_de, for_count=0, duration_en=duration_en, duration_de=duration_de,done=date.today(), project=Project.objects.get(id=self.kwargs['pk']))
            event.save()
            event.responsibles.add(self.request.user)
            for t in form.instance.turbines.all():
                event.turbines.add(t)
                first_date = Date(event=event, turbine=t, date=event.done, status_en=status_en, status_de=status_de, part_of_contract_en=part_of_contract_en, part_of_contract_de=part_of_contract_de, comment_en=comment_en, comment_de=comment_de)
                first_date.save()
        comment = Comment(text='edited project', object_id=self.kwargs['pk'], content_type=ContentType.objects.get(app_label = 'projects', model = 'project'), created=datetime.now(), created_by=self.request.user)
        comment.save()
        return super(ProjectEdit, self).form_valid(form)

def validate_project_name(request):
    project_name = request.POST.get('project_name')
    view_name = request.POST.get('view_name')
    data = {
        'view_name': view_name,
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

class PoolProjectList(PoolTableView):
    model = PoolProject
    table_class = PoolProjectTable
    filter_class = PoolProjectFilter
    template_name = "projects/pool_list.html"

class PoolProjectCreate(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "projects/pool_form.html"
    model = PoolProject
    form_class = PoolProjectForm
    permission_required = 'projects.add_project'
    raise_exception = True

    def form_valid(self, form):
        form.instance.available = True
        form.instance.slug = orig = slugify(str(form.instance.name))
        for x in itertools.count(1):
            if not PoolProject.objects.filter(slug=form.instance.slug).exists():
                break
            form.instance.slug = '%s-%d' % (orig, x)

        form.instance.created = datetime.now()
        form.instance.updated = datetime.now()
        redirect = super(PoolProjectCreate, self).form_valid(form)
        pool_created = self.object
        comment = Comment(text='created pool project', object_id=pool_created.id, content_type=ContentType.objects.get(app_label = 'projects', model = 'poolproject'), created=datetime.now(), created_by=self.request.user)
        comment.save()
        return redirect

class PoolProjectEdit(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = "projects/pool_form.html"
    model = PoolProject
    form_class = PoolProjectForm
    permission_required = 'projects.change_project'
    raise_exception = True

    def form_valid(self, form):
        form.instance.available = True
        form.instance.updated = datetime.now()
        comment = Comment(text='edited pool project', object_id=self.kwargs['pk'], content_type=ContentType.objects.get(app_label = 'projects', model = 'poolproject'), created=datetime.now(), created_by=self.request.user)
        comment.save()
        return super(PoolProjectEdit, self).form_valid(form)

def pool_detail(request, id, slug):
    pool = get_object_or_404(PoolProject, id=id, slug=slug)
    comments = pool.comment.exclude(text__in=["created pool project", "edited pool project"])
    changes = pool.comment.filter(text__in=["created pool project", "edited pool project"])

    return render(request, 'projects/pool_detail.html', {'pool': pool, 'comments': comments, 'changes': changes})

class CommentCreate(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Comment
    form_class = CommentForm
    permission_required = 'projects.can_comment_projects'
    raise_exception = True

    def get_success_url(self):
        if self.kwargs['model'] == 'project':
            project = get_object_or_404(Project, id=self.kwargs['id'])
            success_url = reverse_lazy('projects:project_detail', kwargs={'id': project.id, 'slug': project.slug})
        elif self.kwargs['model'] == 'pool':
            pool = get_object_or_404(PoolProject, id=self.kwargs['id'])
            success_url = reverse_lazy('projects:pool_detail', kwargs={'id': pool.id, 'slug': pool.slug})
        return success_url

    def form_valid(self, form):
        form.instance.available = True
        form.instance.object_id = self.kwargs['id']
        if self.kwargs['model'] == 'project':
            form.instance.content_type = ContentType.objects.get(app_label = 'projects', model = 'project')
        elif self.kwargs['model'] == 'pool':
            form.instance.content_type = ContentType.objects.get(app_label = 'projects', model = 'poolproject')
        form.instance.created = datetime.now()
        form.instance.created_by = self.request.user
        return super(CommentCreate, self).form_valid(form)

class CommentEdit(PermissionRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    permission_required = 'projects.can_comment_projects'
    raise_exception = True

    def get_success_url(self):
        if self.kwargs['model'] == 'project':
            project = get_object_or_404(Project, id=self.kwargs['id'])
            success_url = reverse_lazy('projects:project_detail', kwargs={'id': project.id, 'slug': project.slug})
        elif self.kwargs['model'] == 'pool':
            pool = get_object_or_404(PoolProject, id=self.kwargs['id'])
            success_url = reverse_lazy('projects:pool_detail', kwargs={'id': pool.id, 'slug': pool.slug})
        return success_url

    def form_valid(self, form):
        form.instance.available = True
        form.instance.object_id = self.kwargs['id']
        if self.kwargs['model'] == 'project':
            form.instance.content_type = ContentType.objects.get(app_label = 'projects', model = 'project')
        elif self.kwargs['model'] == 'pool':
            form.instance.content_type = ContentType.objects.get(app_label = 'projects', model = 'poolproject')
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
    events = Event.objects.filter(project=project)
    date_table = DateTable(Date.objects.filter(event__in=events))
    comments = project.comment.exclude(text__in=["created project", "edited project"])
    pool_projects = project.pool_projects.all()
    pool_comments = {}
    if pool_projects:
        for pool in pool_projects:
            pool_comments_qs = Comment.objects.filter(content_type=ContentType.objects.get(app_label = 'projects', model = 'poolproject'), object_id=pool.id).exclude(text__in=["created pool project", "edited pool project"])
            pool_comments_list = []
            for c in pool_comments_qs:
                pool_comments_list.append([c.text, c.created_by, c.created, c.file])
            pool_comments[pool] = pool_comments_list
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

    return render(request, 'projects/detail.html', {'project': project, 'comments': comments, 'pool_comments': pool_comments, 'changes': changes, 'form': driving_form, 'contracts_in_distance_form': contracts_in_distance_form, 'turbines_in_distance_form': turbines_in_distance_form, 'awarding_form': awarding_form, 'reminder': reminder, 'date_table': date_table})

def export_project_coordinates(request, id):
    project = get_object_or_404(Project, id=id)
    filename = "{}-coordinates.xls".format(project.name)
    response = HttpResponse(content_type='applications/vnd.ms-excel')
    response['Content-Disposition'] = 'attachement; filename="{}"'.format(filename)
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("Coordinates")
    columns = [(u'Turbine',5000), (u'Latitude', 5000), (u'Longitude', 5000)]
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num][0], font_style)
        ws.col(col_num).width = columns[col_num][1]
    font_style.alignment.wrap = 1
    for t in project.turbines.all():
        row_num += 1
        row = [t.turbine_id, t.latitude, t.longitude]
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response

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

class Documents(LoginRequiredMixin, SingleTableMixin, ListView):
    model = Document
    table_class = DocumentTable
    template_name = 'projects/documents.html'

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
        if datetime.today().month is not 12:
            last_of_next_month_year = datetime.today().year
            last_of_next_month_month = datetime.today().month + 1
            last_of_next_month_day = mdays[datetime.today().month + 1]
        else:
            last_of_next_month_year = datetime.today().year +1
            last_of_next_month_month = 1
            last_of_next_month_day = 31
        dates = {'first_of_year': datetime(year=datetime.today().year, month=1, day=1).strftime("%Y-%m-%d"), 'last_of_year':datetime(year=datetime.today().year, month=12, day=31).strftime("%Y-%m-%d"), 'first_of_month': datetime(year=datetime.today().year, month=datetime.today().month, day=1).strftime("%Y-%m-%d"), 'last_of_next_month': datetime(year=last_of_next_month_year, month=last_of_next_month_month, day=last_of_next_month_day).strftime("%Y-%m-%d"), 'today': datetime.today().strftime("%Y-%m-%d")}
        context["first_of_year"] = dates["first_of_year"]
        context["last_of_year"] = dates["last_of_year"]
        context["first_of_month"] = dates["first_of_month"]
        context["last_of_next_month"] = dates["last_of_next_month"]
        context["today"] = dates["today"]
        tables = [
            TotalVolumeTable(self.filter.qs.filter(status='Won', start_operation__range=[dates['first_of_year'], dates['last_of_year']])),
            TotalVolumeTable(self.filter.qs.filter(status__in=['Hard Offer', 'Negotiation', 'Final Negotiation'], prob__range=[70, 100], start_operation__range=[dates['first_of_month'], dates['last_of_next_month']])),
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

def create_pdf_parkinformation(request, id, slug):
    project = get_object_or_404(Project, id=id, slug=slug)

    paginated_turbines = Paginator(project.turbines.all(), 7)
    pages = paginated_turbines.page_range
    paginated_turbines_dict = {}
    for i in pages:
        paginated_turbines_dict[i] = paginated_turbines.page(i)

    html_string = render_to_string('projects/reports/parkinformation.html', {'project': project, 'paginated_turbines': paginated_turbines_dict})
    result = HTML(string=html_string).write_pdf()

    response = HttpResponse(result, content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename='+project.name+'_Parkinfoblatt.pdf'
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

    def form_valid(self, form):
        return super(OfferNumberCreate, self).form_valid(form)

def update_offer_number(request):
    offer_number = request.POST.get('offer_number')
    wind_farm = request.POST.get('wind_farm')
    if not request.POST.get('amount') == '':
        amount = int(request.POST.get('amount'))
    else:
        amount = None
    if not request.POST.get('wec_typ') == '':
        wec_typ = int(request.POST.get('wec_typ'))
    else:
        wec_typ = None
    if not request.POST.get('sales_manager') == '':
        sales_manager = int(request.POST.get('sales_manager'))
    else:
        sales_manager = None
    text = request.POST.get('text')

    OfferNumber.objects.filter(number=offer_number).update(wind_farm=wind_farm, amount=amount, sales_manager=sales_manager, text=text)
    if wec_typ != None:
        OfferNumber.objects.get(number=offer_number).wec_typ.add(wec_typ)
    url = reverse('projects:offer_number_list')
    data = {
        'url': url}
    return JsonResponse(data)

def fill_turbines(request):
    wind_farm = request.POST.getlist('wind_farm[]')
    turbines = list(Turbine.objects.filter(wind_farm__in=wind_farm, available=True).values_list('pk', flat=True))
    data = {'turbines': turbines}
    return JsonResponse(data)

def generate_offer_number(request):
    dwt = request.POST.get('dwt')
    today = datetime.now()
    year = today.year
    try:
        if OfferNumber.objects.filter(dwt=dwt).latest().number[5] == "0":
            if OfferNumber.objects.filter(dwt=dwt).latest().number[6] == "0":
                if OfferNumber.objects.filter(dwt=dwt).latest().number[7] == "0":
                    new_offer_number = int(OfferNumber.objects.filter(dwt=dwt).latest().number[8:])+1
                else:
                    new_offer_number = int(OfferNumber.objects.filter(dwt=dwt).latest().number[7:])+1
            else:
                new_offer_number = int(OfferNumber.objects.filter(dwt=dwt).latest().number[6:])+1
        elif OfferNumber.objects.filter(dwt=dwt).latest().number[5:] == "9999":
            new_offer_number = 0
        else:
            new_offer_number = int(OfferNumber.objects.filter(dwt=dwt).latest().number[5:])+1
    except:
        new_offer_number = 0
    if dwt == "DWTS":
        complete_number = "".join(("A", str(year), str(new_offer_number).zfill(4)))
    elif dwt == "DWTX":
        complete_number = "".join(("X", str(year), str(new_offer_number).zfill(4)))
    elif dwt == "DWTOC":
        complete_number = "".join(("O", str(year), str(new_offer_number).zfill(4)))
    elif dwt == "DWTSARL":
        complete_number = "".join(("F", str(year), str(new_offer_number).zfill(4)))
    elif dwt == "DWTUK":
        complete_number = "".join(("B", str(year), str(new_offer_number).zfill(4)))
    elif dwt == "DWTSW":
        complete_number = "".join(("S", str(year), str(new_offer_number).zfill(4)))
    elif dwt == "DWTES":
        complete_number = "".join(("E", str(year), str(new_offer_number).zfill(4)))
    elif dwt == "DWTDK":
        complete_number = "".join(("D", str(year), str(new_offer_number).zfill(4)))
    elif dwt == "DWTUS":
        complete_number = "".join(("U", str(year), str(new_offer_number).zfill(4)))
    elif dwt == "DWTPO":
        complete_number = "".join(("P", str(year), str(new_offer_number).zfill(4)))
    elif dwt == "DWTNED":
        complete_number = "".join(("N", str(year), str(new_offer_number).zfill(4)))
    else:
        complete_number = "".join(("Z", str(year), str(new_offer_number).zfill(4)))

    while complete_number in OfferNumber.objects.all().values_list('number', flat=True):
        if dwt == "DWTS":
            complete_number = "".join(("A", str(year), str(new_offer_number+1).zfill(4)))
        elif dwt == "DWTX":
            complete_number = "".join(("X", str(year), str(new_offer_number+1).zfill(4)))
        elif dwt == "DWTOC":
            complete_number = "".join(("O", str(year), str(new_offer_number+1).zfill(4)))
        elif dwt == "DWTSARL":
            complete_number = "".join(("F", str(year), str(new_offer_number+1).zfill(4)))
        elif dwt == "DWTUK":
            complete_number = "".join(("B", str(year), str(new_offer_number+1).zfill(4)))
        elif dwt == "DWTSW":
            complete_number = "".join(("S", str(year), str(new_offer_number+1).zfill(4)))
        elif dwt == "DWTES":
            complete_number = "".join(("E", str(year), str(new_offer_number+1).zfill(4)))
        elif dwt == "DWTDK":
            complete_number = "".join(("D", str(year), str(new_offer_number+1).zfill(4)))
        elif dwt == "DWTUS":
            complete_number = "".join(("U", str(year), str(new_offer_number+1).zfill(4)))
        elif dwt == "DWTPO":
            complete_number = "".join(("P", str(year), str(new_offer_number+1).zfill(4)))
        elif dwt == "DWTNED":
            complete_number = "".join(("N", str(year), str(new_offer_number+1).zfill(4)))
        else:
            complete_number = "".join(("Z", str(year), str(new_offer_number+1).zfill(4)))

    new_offer_number = OfferNumber.objects.create(number=complete_number, created_by=request.user, dwt=dwt, created=datetime.now())
    data = {
        'new_offer_number': model_to_dict(new_offer_number)}
    return JsonResponse(data)
