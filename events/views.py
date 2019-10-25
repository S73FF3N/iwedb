from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType

from .models import Event, Date
from projects.models import Comment
from projects.forms import CommentForm
from .tables import EventTable, DateTable
from .forms import EventForm, DateForm
from .filters import EventListFilter
from .utils import PagedFilteredTableView

from datetime import timedelta, datetime
import itertools
from django_filters.views import FilterView
from django_tables2 import MultiTableMixin
from django_tables2.config import RequestConfig

def event_detail(request, id):
    event = get_object_or_404(Event, id=id)
    table = DateTable(Date.objects.filter(event=event))
    comments = event.comment.all()

    return render(request, 'events/event_detail.html', {'event':event, 'table': table, 'comments': comments})

def create_dates(request, id):
    event = get_object_or_404(Event, id=id)
    for t in event.turbines.all():
        date = event.done
        first_date = Date(event=event, turbine=t, date=event.done, status="ausstehend")
        first_date.save()
        if event.duration == "Jahre":
            while date < event.done + timedelta(event.for_count*365):
                if event.time_interval == "Jahre":
                    date += timedelta(event.every_count*365)
                if event.time_interval == "Monate":
                    date += timedelta(event.every_count*31)
                if event.time_interval == "Tage":
                    date += timedelta(event.every_count)
                if date < event.done + timedelta(event.for_count*365):
                    next_date = Date(event=event, turbine=t, date=date, status="ausstehend")
                    next_date.save()
        if event.duration == "Monate":
            while date < event.done + timedelta(event.for_count*31):
                if event.time_interval == "Jahre":
                    date += timedelta(event.every_count*365)
                if event.time_interval == "Monate":
                    date += timedelta(event.every_count*31)
                if event.time_interval == "Tage":
                    date += timedelta(event.every_count)
                if date < event.done + timedelta(event.for_count*365):
                    next_date = Date(event=event, turbine=t, date=date, status="ausstehend")
                    next_date.save()
        else:
            while date < event.done + timedelta(event.for_count):
                if event.time_interval == "Jahre":
                    date += timedelta(event.every_count*365)
                if event.time_interval == "Monate":
                    date += timedelta(event.every_count*31)
                if event.time_interval == "Tage":
                    date += timedelta(event.every_count)
                if date < event.done + timedelta(event.for_count*365):
                    next_date = Date(event=event, turbine=t, date=date, status="ausstehend")
                    next_date.save()
    return HttpResponseRedirect(reverse_lazy('events:event_detail', kwargs={'id': event.id}))


class EventList(PagedFilteredTableView):
    template_name = "events/event_list.html"
    model = Event
    table_class = EventTable
    filter_class = EventListFilter

class EventAndDateList(LoginRequiredMixin, MultiTableMixin, FilterView):
    model = Event
    filterset_class = EventListFilter
    template_name = 'events/event_list.html'

    def get_queryset(self,*args, **kwargs):
        qs = super(EventAndDateList, self).get_queryset().select_related('responsible').prefetch_related('turbines', 'turbines__wind_farm')
        self.filter = self.filterset_class(self.request.GET, queryset=qs)
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super(MultiTableMixin, self).get_context_data(**kwargs)
        dates = {'in_six_month': (datetime.now() + timedelta(days=182)).strftime("%Y-%m-%d"), 'six_month_ago': (datetime.now() - timedelta(days=182)).strftime("%Y-%m-%d")}
        context["six_month_ago"] = dates["six_month_ago"]
        context["in_six_month"] = dates["in_six_month"]
        tables = [
            EventTable(self.filter.qs),
            DateTable(Date.objects.filter(event__in=self.filter.qs, status='ausstehend', date__range=[dates['six_month_ago'], dates['in_six_month']])),
            DateTable(Date.objects.filter(event__in=self.filter.qs, status='geplant', date__range=[dates['six_month_ago'], dates['in_six_month']])),
                ]
        table_counter = itertools.count()
        for table in tables:
            table.prefix = table.prefix or self.table_prefix.format(next(table_counter))
            RequestConfig(self.request, paginate=self.get_table_pagination(table)).configure(table)
            context[self.get_context_table_name(table)] = list(tables)
        return context

class EventCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = "events/event_form.html"
    model = Event
    form_class = EventForm
    raise_exception = True

    def get_success_url(self):
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
            form.save()
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
