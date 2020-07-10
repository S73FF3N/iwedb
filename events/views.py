from weasyprint import HTML

from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string

from wind_farms.models import WindFarm
from .models import Event, Date
from projects.models import Comment
from projects.forms import CommentForm
from .tables import EventTable, DateTable, DateTableEdit,  DateTableKM, SelectDatesTable
from .forms import EventForm, DateForm, DateFilterForm, ChangeMultipleDatesForm, ChangeAllDatesForm, CreateOrderForm
from .filters import EventListFilter

from datetime import timedelta, datetime
import itertools
import xlwt
from django_filters.views import FilterView
from django_tables2 import MultiTableMixin
from django_tables2.config import RequestConfig

def event_detail(request, id):
    event = get_object_or_404(Event, id=id)
    table = DateTableEdit(Date.objects.filter(event=event))
    comments = event.comment.all()

    return render(request, 'events/event_detail.html', {'event':event, 'table': table, 'comments': comments})

def create_dates(request, id):
    event = get_object_or_404(Event, id=id)
    for t in event.turbines.all():
        date = event.done
        status = 'remaining'
        first_date = Date(event=event, turbine=t, date=event.done, status=status)
        first_date.save()
        if event.duration == 'years':
            while date < event.done + timedelta(event.for_count*365):
                if event.time_interval == 'years':
                    date += timedelta(event.every_count*365)
                if event.time_interval == 'month':
                    date += timedelta(event.every_count*31)
                if event.time_interval == 'days':
                    date += timedelta(event.every_count)
                if date < event.done + timedelta(event.for_count*365):
                    next_date = Date(event=event, turbine=t, date=date, status=status)
                    next_date.save()
        elif event.duration == 'month':
            while date < event.done + timedelta(event.for_count*31):
                if event.time_interval == 'years':
                    date += timedelta(event.every_count*365)
                if event.time_interval == 'month':
                    date += timedelta(event.every_count*31)
                if event.time_interval == 'days':
                    date += timedelta(event.every_count)
                if date < event.done + timedelta(event.for_count*365):
                    next_date = Date(event=event, turbine=t, date=date, status=status)
                    next_date.save()
        elif event.duration == 'days':
            while date < event.done + timedelta(event.for_count):
                if event.time_interval == 'years':
                    date += timedelta(event.every_count*365)
                if event.time_interval == 'month':
                    date += timedelta(event.every_count*31)
                if event.time_interval == 'days':
                    date += timedelta(event.every_count)
                if date < event.done + timedelta(event.for_count*365):
                    next_date = Date(event=event, turbine=t, date=date, status=status)
                    next_date.save()
    return HttpResponseRedirect(reverse_lazy('events:event_detail', kwargs={'id': event.id}))

def ChangeAllDates(request, pk):
    event_object = get_object_or_404(Event, pk=pk)
    form = ChangeAllDatesForm(event_pk=pk)

    if request.method == 'POST':
        form = ChangeAllDatesForm(request.POST, event_pk=pk)

        if form.is_valid():
            for date in form.cleaned_data['dates']:
                if form.cleaned_data['execution_date']:
                    date.execution_date = form.cleaned_data['execution_date']
                if form.cleaned_data['service_provider']:
                    date.service_provider = form.cleaned_data['service_provider']
                if form.cleaned_data['order_date']:
                    date.comment = form.cleaned_data['order_date']
                if form.cleaned_data['status']:
                    date.status = form.cleaned_data['status']
                if form.cleaned_data['comment']:
                    date.comment = form.cleaned_data['comment']
                if form.cleaned_data['next_dates_based_on_execution_date'] and form.cleaned_data['execution_date']:
                    date.calculate_next_dates_based_on_execution_date()
                else:
                    return render(request, 'events/change-multiple-dates.html', {'form': form})

                date.save()
            return HttpResponseRedirect(reverse_lazy('events:event_detail', kwargs={'id': event_object.id}))
    return render(request, 'events/change-multiple-dates.html', {'form': form})

def ChangeMultipleDates(request, pk, date_string):
    dates = date_string.split("+")
    event_object = get_object_or_404(Event, pk=pk)
    form = ChangeMultipleDatesForm(event_pk=pk, dates=dates)

    if request.method == 'POST':
        form = ChangeMultipleDatesForm(request.POST, event_pk=pk, dates=dates)

        if form.is_valid():
            for date in form.cleaned_data['dates']:
                if form.cleaned_data['execution_date']:
                    date.execution_date = form.cleaned_data['execution_date']
                if form.cleaned_data['service_provider']:
                    date.service_provider = form.cleaned_data['service_provider']
                if form.cleaned_data['order_date']:
                    date.comment = form.cleaned_data['order_date']
                if form.cleaned_data['status']:
                    date.status = form.cleaned_data['status']
                if form.cleaned_data['comment']:
                    date.comment = form.cleaned_data['comment']
                if form.cleaned_data['next_dates_based_on_execution_date'] and form.cleaned_data['execution_date']:
                    date.calculate_next_dates_based_on_execution_date()
                else:
                    return render(request, 'events/change-multiple-dates.html', {'form': form})

                date.save()

            return HttpResponseRedirect(reverse_lazy('events:event_detail', kwargs={'id': event_object.id}))
    return render(request, 'events/change-multiple-dates.html', {'form': form})

class EventAndDateList(LoginRequiredMixin, MultiTableMixin, FilterView):
    model = Event
    filterset_class = EventListFilter
    template_name = 'events/event_list.html'

    start_date = (datetime.now() - timedelta(days=365))
    end_date = (datetime.now() + timedelta(days=365))

    def get(self, request, *args, **kwargs):
        form = DateFilterForm(request.GET)
        if form.is_valid():
            self.start_date = form.cleaned_data["date_start"]
            self.end_date = form.cleaned_data["date_end"]
        return super(EventAndDateList, self).get(request, *args, **kwargs)

    def get_queryset(self,*args, **kwargs):
        qs = super(EventAndDateList, self).get_queryset().filter(responsibles__groups__name__in=["Technical Operations"]).prefetch_related('turbines', 'turbines__wind_farm', 'responsibles')
        self.filter = self.filterset_class(self.request.GET, queryset=qs)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super(MultiTableMixin, self).get_context_data(**kwargs)
        context["count_qs"] = self.filter.qs.count()
        not_dated = [x for x in self.filter.qs if x._dated() == _('no')]
        context["count_not_dated"] = len(not_dated)
        context["count_date_qs"] = Date.objects.filter(event__in=self.filter.qs).count()
        action_required = [x for x in Date.objects.filter(event__in=self.filter.qs) if x._traffic_light() == "red" or x._traffic_light() == "orange"]
        context["count_action_required"] = len(action_required)
        context["date_filter_form"] = DateFilterForm()
        dates = {'end_date': self.end_date, 'start_date': self.start_date}
        context["start_date"] = dates["start_date"]
        context["end_date"] = dates["end_date"]
        tables = [
            EventTable(self.filter.qs.filter(responsibles__groups__name__in=["Technical Operations"])),
            DateTable(Date.objects.filter(event__in=self.filter.qs, status='remaining', event__project__isnull=True, date__range=[dates['start_date'], dates['end_date']])),
            DateTable(Date.objects.filter(event__in=self.filter.qs, status='ordered', event__project__isnull=True, date__range=[dates['start_date'], dates['end_date']])),
            DateTable(Date.objects.filter(event__in=self.filter.qs, status='confirmed', event__project__isnull=True, date__range=[dates['start_date'], dates['end_date']])),
            DateTable(Date.objects.filter(event__in=self.filter.qs, status='scheduled', event__project__isnull=True, date__range=[dates['start_date'], dates['end_date']])),
            DateTable(Date.objects.filter(event__in=self.filter.qs, status='executed', event__project__isnull=True, date__range=[dates['start_date'], dates['end_date']])),
            DateTable(Date.objects.filter(event__in=self.filter.qs, status='report received', event__project__isnull=True, date__range=[dates['start_date'], dates['end_date']])),
                ]
        table_counter = itertools.count()
        for table in tables:
            table.prefix = table.prefix or self.table_prefix.format(next(table_counter))
            RequestConfig(self.request, paginate=self.get_table_pagination(table)).configure(table)
            context[self.get_context_table_name(table)] = list(tables)

        return context

    @classmethod
    def export(cls, request):
        filename = "date-export-{}.xls".format(datetime.now().replace(microsecond=0).isoformat())
        response = HttpResponse(content_type='applications/vnd.ms-excel')
        response['Content-Disposition'] = 'attachement; filename="{}"'.format(filename)
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet("Date Overview")
        row_num = 0
        columns = [(_('Scheduled Date'),5000), (_('Expert Report'), 5000), (_('Wind Farm'), 5000), (_('Turbine'), 3000), (_('Status'), 5000), (_('Service Provider'), 3000), (_('Contract'), 3000), (_('Execution Date'), 3000), (_('Comment'), 7000), (_('Responsible'), 5000), (_('Comissioning Year'), 5000), (_('Month'), 5000),(_('Day'), 5000), (_('Every'), 3000), (_('Interval'), 5000)]#, (_('Part Of Contract'), 3000)
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, str(columns[col_num][0]), font_style)
            ws.col(col_num).width = columns[col_num][1]
        font_style = xlwt.XFStyle()
        font_style.alignment.wrap = 1
        date_style = xlwt.XFStyle()
        date_style.num_format_str = 'D-MMM-YY'
        font_styles = [date_style, font_style, font_style, font_style, font_style, font_style, font_style, font_style, font_style, font_style, font_style, font_style, font_style, font_style, font_style]#, font_style]
        queryset = Date.objects.all()
        for obj in queryset:
            row_num += 1
            if obj.service_provider == None:
                service_provider = None
            else:
                service_provider = obj.service_provider.name
            try:
                date_wind_farm_name = obj.date_wind_farm_name
            except WindFarm.DoesNotExist:
                date_wind_farm_name = _("No wind farm name specified")
            row = [obj.date, obj.event.title, date_wind_farm_name, obj.turbine.turbine_id, str(obj.status), service_provider, str(obj.contract_scope), obj.execution_date, obj.comment, obj.responsible.__str__(), obj.turbine.commisioning_year, obj.turbine.commisioning_month, obj.turbine.commisioning_day, obj.event.every_count, str(obj.event.time_interval)]#, str(obj.part_of_contract)
            for col_num in range(len(row)):
                ws.write(row_num, col_num, str(row[col_num]), font_styles[col_num])
        wb.save(response)
        return response

class KMEventAndDateList(LoginRequiredMixin, MultiTableMixin, FilterView):
    model = Event
    filterset_class = EventListFilter
    template_name = 'events/km_event_list.html'

    start_date = (datetime.now() - timedelta(days=365))
    end_date = (datetime.now() + timedelta(days=365))

    def get(self, request, *args, **kwargs):
        form = DateFilterForm(request.GET)
        if form.is_valid():
            self.start_date = form.cleaned_data["date_start"]
            self.end_date = form.cleaned_data["date_end"]
        return super(KMEventAndDateList, self).get(request, *args, **kwargs)

    def get_queryset(self,*args, **kwargs):
        qs = super(KMEventAndDateList, self).get_queryset().filter(responsibles__groups__name__in=["Customer Relations"]).prefetch_related('turbines', 'turbines__wind_farm', 'responsibles')
        self.filter = self.filterset_class(self.request.GET, queryset=qs)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super(MultiTableMixin, self).get_context_data(**kwargs)
        context["count_qs"] = self.filter.qs.count()
        not_dated = [x for x in self.filter.qs if x._dated() == _('no')]
        context["count_not_dated"] = len(not_dated)
        context["count_date_qs"] = Date.objects.filter(event__in=self.filter.qs).count()
        action_required = [x for x in Date.objects.filter(event__in=self.filter.qs) if x._traffic_light() == "red" or x._traffic_light() == "orange"]
        context["count_action_required"] = len(action_required)
        context["date_filter_form"] = DateFilterForm()
        dates = {'end_date': self.end_date, 'start_date': self.start_date}
        context["start_date"] = dates["start_date"]
        context["end_date"] = dates["end_date"]
        tables = [
            EventTable(self.filter.qs.filter(responsibles__groups__name__in=["Customer Relations"])),
            DateTableKM(Date.objects.filter(event__in=self.filter.qs, status='remaining', event__project__isnull=True, date__range=[dates['start_date'], dates['end_date']])),
            DateTableKM(Date.objects.filter(event__in=self.filter.qs, status='ordered', event__project__isnull=True, date__range=[dates['start_date'], dates['end_date']])),
            DateTableKM(Date.objects.filter(event__in=self.filter.qs, status='report received', event__project__isnull=True, date__range=[dates['start_date'], dates['end_date']])),
            DateTableKM(Date.objects.filter(event__in=self.filter.qs, status='invoice received', event__project__isnull=True, date__range=[dates['start_date'], dates['end_date']])),
            ]
        table_counter = itertools.count()
        for table in tables:
            table.prefix = table.prefix or self.table_prefix.format(next(table_counter))
            RequestConfig(self.request, paginate=self.get_table_pagination(table)).configure(table)
            context[self.get_context_table_name(table)] = list(tables)
        return context

    @classmethod
    def export(cls, request):
        filename = "date-export-{}.xls".format(datetime.now().replace(microsecond=0).isoformat())
        response = HttpResponse(content_type='applications/vnd.ms-excel')
        response['Content-Disposition'] = 'attachement; filename="{}"'.format(filename)
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet("Date Overview")
        row_num = 0
        columns = [(_('Scheduled Date'),5000), (_('Expert Report'), 5000), (_('Wind Farm'), 5000), (_('Turbine'), 3000), (_('Status'), 5000), (_('Service Provider'), 3000), (_('Order Date'), 3000),(_('Contract'), 3000), (_('Execution Date'), 3000), (_('Comment'), 7000), (_('Responsible'), 5000), (_('Comissioning Year'), 5000), (_('Month'), 5000),(_('Day'), 5000), (_('Every'), 3000), (_('Interval'), 5000)]#, (_('Part Of Contract'), 3000)
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, str(columns[col_num][0]), font_style)
            ws.col(col_num).width = columns[col_num][1]
        font_style = xlwt.XFStyle()
        font_style.alignment.wrap = 1
        date_style = xlwt.XFStyle()
        date_style.num_format_str = 'D-MMM-YY'
        font_styles = [date_style, font_style, font_style, font_style, font_style, font_style, date_style, font_style, font_style, font_style, font_style, font_style, font_style, font_style, font_style, font_style]#, font_style]
        queryset = Date.objects.all()
        for obj in queryset:
            row_num += 1
            if obj.service_provider == None:
                service_provider = None
            else:
                service_provider = obj.service_provider.name
            try:
                date_wind_farm_name = obj.date_wind_farm_name
            except WindFarm.DoesNotExist:
                date_wind_farm_name = _("No wind farm name specified")
            row = [obj.date, obj.event.title, date_wind_farm_name, obj.turbine.turbine_id, str(obj.status), service_provider, obj.order_date, str(obj.contract_scope), obj.execution_date, obj.comment, obj.responsible.__str__(), obj.turbine.commisioning_year, obj.turbine.commisioning_month, obj.turbine.commisioning_day, obj.event.every_count, str(obj.event.time_interval)]#, str(obj.part_of_contract)
            for col_num in range(len(row)):
                ws.write(row_num, col_num, str(row[col_num]), font_styles[col_num])
        wb.save(response)
        return response

class EventCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "events/event_form.html"
    model = Event
    form_class = EventForm
    raise_exception = True

    def get_success_url(self):
        if "Customer Relations" in self.request.user.groups.values_list('name',flat = True):
            success_url = reverse_lazy('events:km_event_list')
        else:
            success_url = reverse_lazy('events:event_list')
        return success_url

class EventEdit(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Event
    form_class = EventForm
    raise_exception = True

class DateEdit(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Date
    form_class = DateForm
    raise_exception = True
    template_name = "events/date_form.html"

    def get_form_kwargs(self, **kwargs):
        kwargs = super(DateEdit, self).get_form_kwargs()
        redirect = self.request.GET.get('next')
        self.success_url = redirect
        if redirect:
            if 'initial' in kwargs.keys():
                kwargs['initial'].update({'next': redirect})
            else:
                kwargs['initial'] = {'next': redirect}
        return kwargs

    def form_valid(self, form):
        if form.cleaned_data["next_dates_based_on_execution_date"] == True:
            form.save()
            date = self.get_object()
            date.calculate_next_dates_based_on_execution_date()
        redirect = form.cleaned_data.get('next')
        if redirect:
            self.success_url = redirect
        return super(DateEdit, self).form_valid(form)

def DateCreate(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    initial_data = {'event':event}
    if request.method == 'POST':
        form = DateForm(request.POST or None, initial=initial_data)
        if form.is_valid():
            new_date = form.save(commit=False)
            new_date.event = event
            new_date.save()
            return HttpResponseRedirect(reverse_lazy('events:event_detail', kwargs={'id': event_id}))
    else:
        form = DateForm(initial=initial_data)
    return render(request, 'events/date_form.html', {'form':form})

def DateDelete(request, date):
    date_to_delete = get_object_or_404(Date, id=date)
    event = date_to_delete.event
    date_to_delete.delete()

    if reverse('events:event_list') in request.META.get('HTTP_REFERER'):
        success_url = HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        success_url = redirect('events:event_detail', id=event.id)
    return success_url

class CommentCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Comment
    form_class = CommentForm
    templete_name = "projects/comment_form.html"
    raise_exception = True

    def get_success_url(self):
        event = get_object_or_404(Event, id=self.kwargs['event_id'])
        success_url = reverse_lazy('events:event_detail', kwargs={'id': event.id})
        return success_url

    def form_valid(self, form):
        form.instance.available = True
        form.instance.object_id = self.kwargs['event_id']
        form.instance.content_type = ContentType.objects.get(app_label = 'events', model = 'event')
        form.instance.created = datetime.now()
        form.instance.created_by = self.request.user
        return super(CommentCreate, self).form_valid(form)

class CommentEdit(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    raise_exception = True

    def get_success_url(self):
        event = get_object_or_404(Event, id=self.kwargs['event_id'])
        success_url = reverse_lazy('events:event_detail', kwargs={'id': event.id})
        return success_url

    def form_valid(self, form):
        form.instance.available = True
        form.instance.object_id = self.kwargs['event_id']
        form.instance.content_type = ContentType.objects.get(app_label = 'events', model = 'event')
        return super(CommentEdit, self).form_valid(form)

def select_dates(request, event_pk):
    event = get_object_or_404(Event, id=event_pk)
    table = SelectDatesTable(Date.objects.filter(event=event, status="remaining"))

    return render(request, 'events/select_dates.html', {'event':event, 'table': table})

def create_order_no_dates(request, event_pk):
    messages.info(request, _('Please select a date from the table.'))
    return HttpResponseRedirect(reverse_lazy('events:select_dates', kwargs={'event_pk': event_pk}))

def create_order(request, event_pk, date_string):
    if request.method == 'POST':
        form = CreateOrderForm(request.POST)
        if form.is_valid():
            return export_order(request, form.cleaned_data)
    else:
        event = get_object_or_404(Event, id=event_pk)
        date_id_list = date_string.split("+")
        dates = set()
        wind_farm_name = event.event_windfarm_name
        wind_farm = get_object_or_404(WindFarm, name=wind_farm_name)

        wec_manufacturers = set()
        wec_type_names = set()
        hub_heights = set()
        turbine_serials = set()
        tec_operators = set()
        output_power = set()

        for date_id in date_id_list:
            date = get_object_or_404(Date, id=date_id)
            dates.add(date)
            turbine = date.turbine
            wec_manufacturers.add(turbine.wec_typ.manufacturer.name)
            wec_type_names.add(turbine.wec_typ.name)
            output_power.add(str(turbine.wec_typ.output_power))
            hub_heights.add(str(turbine.hub_height))
            turbine_serials.add(turbine.turbine_id)
            tec_operators.update(map(str, turbine.tec_operators()))

        initial_data = {}
        initial_data["ordered_by"] = """Kundenmanagement\nDeutsche Windtechnik X-Service GmbH, Heideweg 2-4, 49086 Osnabrück\nEmail: kundenmanagement@deutsche-windtechnik.com"""

        initial_data["wind_farm_desc"] = wind_farm_name
        initial_data["wind_farm_wec_count"] = len(turbine_serials)
        initial_data["wind_farm_wka"] = ", ".join(turbine_serials)
        initial_data["event_type"] = event.title
        initial_data["documents"] = "Kundenmanagement"

        initial_data["postcode"] = wind_farm.postal_code
        initial_data["location"] = wind_farm.city
        initial_data["wec_manufacturer"] = ", ".join(wec_manufacturers)
        initial_data["wec_type"] = ",".join(wec_type_names)
        initial_data["rated_capacity"] = ", ".join(output_power)
        initial_data["hub_height"] = ",".join(hub_heights)
        initial_data["wec_count"] = len(turbine_serials)
        initial_data["serials"] = ", ".join(turbine_serials)

        initial_data["alarm_system"] = 'No information'

        initial_data["company"] = ",".join(tec_operators)

        form = CreateOrderForm(initial=initial_data)
    return render(request, 'events/create_order_form.html', {'form': form})

def export_order(request, form_data):
    if "\n" in form_data["ordered_by"]:
        form_data["ordered_by_b"], form_data["ordered_by"] = form_data["ordered_by"].split("\n", 1)
    if " " in form_data["documents"]:
        form_data["documents_b"], form_data["documents"] = form_data["documents"].split(" ", 1)

    order_confirmation_fields = {"order_accepted", "planned_execution", "name", "confirmation_comment"}
    for key, value in form_data.items():
        if key not in order_confirmation_fields and (value == None or value == ""):
            form_data[key] = "Keine Angabe"
        elif key in order_confirmation_fields and value == None:
            form_data[key] = " "

    html_string = render_to_string('events/export_order.html', {'form_data': form_data,})
    result = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf()

    response = HttpResponse(result, content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=Bestellformular.pdf'
    return response