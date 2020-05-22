from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from .models import Event, Date, translation_dict
from projects.models import Comment
from projects.forms import CommentForm
from .tables import EventTable, DateTable, DateTableEdit,  DateTableKM
from .forms import EventForm, DateForm, DateFilterForm, ChangeMultipleDatesForm, ChangeAllDatesForm
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

                date.save()
            return HttpResponseRedirect(reverse_lazy('events:event_detail', kwargs={'id': event_object.id}))
    return render(request, 'events/change-all-dates.html', {'form': form})

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
                if form.cleaned_data['next_dates_based_on_execution_date']:
                    date.calculate_next_dates_based_on_execution_date()

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
            #DateTable(Date.objects.filter(event__in=self.filter.qs, status=_('invoice received'), event__project__isnull=True, date__range=[dates['start_date'], dates['end_date']])),
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
            ws.write(row_num, col_num, columns[col_num][0], font_style)
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
            row = [obj.date, obj.event.title, obj.date_wind_farm_name, obj.turbine.turbine_id, str(obj.status), service_provider, str(obj.contract_scope), obj.execution_date, obj.comment, obj.responsible.__str__(), obj.turbine.commisioning_year, obj.turbine.commisioning_month, obj.turbine.commisioning_day, obj.event.every_count, str(obj.event.time_interval)]#, str(obj.part_of_contract)
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_styles[col_num])
        wb.save(response)
        return response

class KMEventAndDateList(LoginRequiredMixin, MultiTableMixin, FilterView):
    model = Event
    filterset_class = EventListFilter
    template_name = 'events/km_event_list.html'

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
        dates = {'in_three_month': (datetime.now() + timedelta(days=90)), 'today': datetime.now(), 'one_month_ago': (datetime.now() - timedelta(days=30))}
        context["today"] = dates["today"]
        context["in_three_month"] = dates["in_three_month"]
        context["one_month_ago"] = dates["one_month_ago"]
        tables = [
            EventTable(self.filter.qs.filter(responsibles__groups__name__in=["Customer Relations"])),
            DateTableKM(Date.objects.filter(event__in=self.filter.qs, status='remaining', event__project__isnull=True, date__range=[dates['today'], dates['in_three_month']])),
            DateTableKM(Date.objects.filter(event__in=self.filter.qs, status='ordered', event__project__isnull=True, date__lte=dates['one_month_ago'])),
            DateTableKM(Date.objects.filter(event__in=self.filter.qs, status='report received', event__project__isnull=True)),
            DateTableKM(Date.objects.filter(event__in=self.filter.qs, status='invoice received', event__project__isnull=True)),
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
            ws.write(row_num, col_num, columns[col_num][0], font_style)
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
            row = [obj.date, obj.event.title, obj.date_wind_farm_name, obj.turbine.turbine_id, str(obj.status), service_provider, obj.order_date, str(obj.contract_scope), obj.execution_date, obj.comment, obj.responsible.__str__(), obj.turbine.commisioning_year, obj.turbine.commisioning_month, obj.turbine.commisioning_day, obj.event.every_count, str(obj.event.time_interval)]#, str(obj.part_of_contract)
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_styles[col_num])
        wb.save(response)
        return response

class EventCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "events/event_form.html"
    model = Event
    form_class = EventForm
    raise_exception = True
    translation_dict = translation_dict #überflüssig?

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
