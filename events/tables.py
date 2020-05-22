import django_tables2 as dt2

from .models import Event, Date

from django.utils.translation import ugettext_lazy as _

class EventTable(dt2.Table):
    title = dt2.LinkColumn(None)
    event_windfarm_name = dt2.Column(verbose_name=_('Wind Farm'), orderable=False)
    responsible_names = dt2.Column(verbose_name=_("Responsible"))
    dated = dt2.Column(verbose_name=_("dated"), orderable=False)

    class Meta:
        model = Event
        fields =('title', 'event_windfarm_name', 'turbines', 'every_count', 'time_interval', 'for_count', 'duration', 'responsible_names', 'dated')
        attrs = {"class": "windfarms"}
        row_attrs = {'dated': lambda record: record.dated}
        per_page = 20
        empty_text = _("There are no events matching the search criteria...")

class DateTable(dt2.Table):

    edit = dt2.TemplateColumn(template_name='events/date_update_column.html', verbose_name=_("Edit"))
    delete = dt2.TemplateColumn(template_name='events/date_delete_column.html', verbose_name=_("Delete"))
    wind_farm = dt2.Column(verbose_name=_("Wind Farm"), accessor='date_wind_farm_name', orderable=False)
    date = dt2.DateColumn(format ='d M Y')
    execution_date = dt2.DateColumn(format ='d M Y')
    turbine_commissioning = dt2.Column(verbose_name=_('Comissioning'), orderable=False)
    contract_scope = dt2.Column(verbose_name=_("Contract"), orderable=False)
    responsible = dt2.Column(verbose_name=_("Responsible"))
    event__title = dt2.Column(accessor='event.title', verbose_name=_("Type"))

    class Meta:
        model = Date
        fields =('date', 'event__title', 'wind_farm', 'turbine', 'turbine_commissioning', 'status', 'service_provider', 'contract_scope', 'execution_date', 'comment', 'responsible', 'edit', 'delete')
        attrs = {"class": "windfarms"}
        row_attrs = {'traffic_light': lambda record: record.traffic_light}
        per_page = 20
        empty_text = _("There are no events matching the search criteria...")

class DateTableEdit(dt2.Table):

    edit = dt2.TemplateColumn(template_name='events/date_update_column.html', verbose_name=_("Edit"))
    delete = dt2.TemplateColumn(template_name='events/date_delete_column.html', verbose_name=_("Delete"))
    mark_to_edit = dt2.TemplateColumn(template_name='events/date_checkbox_column.html', attrs={"td": {"style": "text-align:center;"}}, verbose_name=" ")
    wind_farm = dt2.Column(verbose_name=_("Wind Farm"), accessor='date_wind_farm_name', orderable=False)
    date = dt2.DateColumn(format ='d M Y')
    execution_date = dt2.DateColumn(format ='d M Y')
    turbine_commissioning = dt2.Column(verbose_name=_('Comissioning'), orderable=False)
    contract_scope = dt2.Column(verbose_name=_("Contract"), orderable=False)
    responsible = dt2.Column(verbose_name=_("Responsible"))
    event__title = dt2.Column(accessor='event.title', verbose_name=_("Type"))

    class Meta:
        model = Date
        fields =('mark_to_edit', 'date', 'event__title', 'wind_farm', 'turbine', 'turbine_commissioning', 'status', 'service_provider', 'contract_scope', 'execution_date', 'comment', 'responsible', 'edit', 'delete')
        attrs = {"class": "windfarms"}
        row_attrs = {'traffic_light': lambda record: record.traffic_light}
        per_page = 20
        empty_text = _("There are no events matching the search criteria...")

class DateTableKM(dt2.Table):

    edit = dt2.TemplateColumn(template_name='events/date_update_column.html', verbose_name=_("Edit"))
    delete = dt2.TemplateColumn(template_name='events/date_delete_column.html', verbose_name=_("Delete"))
    wind_farm = dt2.Column(verbose_name=_("Wind Farm"), accessor='date_wind_farm_name', orderable=False)
    date = dt2.DateColumn(format ='d M Y')
    execution_date = dt2.DateColumn(format ='d M Y')
    order_date = dt2.DateColumn(format ='d M Y')
    turbine_commissioning = dt2.Column(verbose_name=_('Comissioning'), orderable=False)
    contract_scope = dt2.Column(verbose_name=_("Contract"), orderable=False)
    responsible = dt2.Column(verbose_name=_("Responsible"))
    event__title = dt2.Column(accessor='event.title', verbose_name=_("Type"))

    class Meta:
        model = Date
        fields =('date', 'event__title', 'wind_farm', 'turbine', 'turbine_commissioning', 'status', 'service_provider', 'order_date', 'contract_scope', 'execution_date', 'comment', 'responsible', 'edit', 'delete')
        attrs = {"class": "windfarms"}
        row_attrs = {'traffic_light': lambda record: record.traffic_light}
        per_page = 20
        empty_text = _("There are no events matching the search criteria...")