import django_tables2 as dt2

from .models import Event, Date

class EventTable(dt2.Table):
    title = dt2.LinkColumn(None)
    wind_farm = dt2.Column(verbose_name='Windpark', orderable=False)
    responsible = dt2.Column(verbose_name="Verantwortlich")

    class Meta:
        model = Event
        fields =('title', 'wind_farm', 'turbines', 'every_count', 'time_interval', 'for_count', 'duration', 'responsible')
        attrs = {"class": "windfarms"}
        per_page = 20
        empty_text = "There are no events matching the search criteria..."

class DateTable(dt2.Table):

    edit = dt2.TemplateColumn(template_name='events/date_update_column.html', verbose_name="Ändern")
    delete = dt2.TemplateColumn(template_name='events/date_delete_column.html', verbose_name="Löschen")

    class Meta:
        model = Date
        fields =('date', 'event', 'turbine', 'status', 'service_provider', 'part_of_contract', 'execution_date', 'comment', 'edit', 'delete')
        attrs = {"class": "windfarms"}
        row_attrs = {'traffic_light': lambda record: record.traffic_light}
        per_page = 20
        empty_text = "There are no events matching the search criteria..."