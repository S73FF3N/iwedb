from django_tables2 import SingleTableView
from django.db.models import Count, Min, Case, When
from django.http import HttpResponse
from django.core import serializers
from django.utils.translation import ugettext_lazy as _

import serpy
from graphos.sources.simple import SimpleDataSource
from graphos.renderers.gchart import PieChart, BarChart
from datetime import datetime
import xlwt

from .models import ServiceLocation, Turbine, Contract

class TurbineSerializer(serpy.Serializer):
    pk = serpy.IntField()
    slug = serpy.Field()
    latitude = serpy.Field()
    longitude = serpy.Field()
    turbine_id = serpy.Field()
    wec_typ_name = serpy.Field()

class ContractSerializer(serpy.Serializer):
    pk = serpy.IntField()
    name = serpy.Field()
    contracted_windfarm_name = serpy.Field()
    contract_coordinates = serpy.Field()
    amount_turbines = serpy.Field()
    contracted_wec_types_name = serpy.Field()

class ServiceLocationSerializer(serpy.Serializer):
    name = serpy.Field()
    dwt = serpy.Field()
    supported_technology_name = serpy.Field()
    latitude = serpy.Field()
    longitude = serpy.Field()

class ProjectSerializer(serpy.Serializer):
    pk = serpy.IntField()
    slug = serpy.Field()
    project_coordinates = serpy.Field()
    name = serpy.Field()
    amount_turbines = serpy.Field()
    project_wec_types_name = serpy.Field()

class PagedFilteredTableView(SingleTableView):
    filter_class = None
    context_filter_name = 'filter'

    def get_queryset(self, **kwargs):
        qs = super(PagedFilteredTableView, self).get_queryset().filter(available=True).select_related('wec_typ', 'wec_typ__manufacturer', 'wind_farm')
        self.filter = self.filter_class(self.request.GET, queryset=qs)
        return self.filter.qs

    def get_context_data(self, **kwargs):
	    context = super(PagedFilteredTableView, self).get_context_data()
	    context[self.context_filter_name] = self.filter

	    queryset = self.filter.qs

	    models = queryset.values('wec_typ__name').annotate(wtgs=Count('wec_typ__name')).order_by('-wtgs')
	    wec_type_datalist = [[_('WEC Type'), _('Amount WTG')]]
	    for wec in models[:10]:
	        temp = [wec['wec_typ__name'], wec['wtgs']]
	        wec_type_datalist.append(temp)
	    wec_type_data_source = SimpleDataSource(data=wec_type_datalist)
	    wec_type_chart = PieChart(wec_type_data_source, html_id='wec_type_chart', options = { 'title': _('Turbine Type by Amount of WTG'), 'is3D': 'true', 'pieSliceText': 'label'})
	    context['wec_type_chart'] = wec_type_chart

	    manufacturers = queryset.values('wec_typ__manufacturer__name').annotate(wtgs=Count('wec_typ__manufacturer__name')).order_by('-wtgs')
	    manufacturers_datalist = [[_('Manufacturer'), _('Amount WTG')]]
	    for wec in manufacturers[:10]:
	        temp = [wec['wec_typ__manufacturer__name'], wec['wtgs']]
	        manufacturers_datalist.append(temp)
	    manufacturers_data_source = SimpleDataSource(data=manufacturers_datalist)
	    manufacturers_chart = PieChart(manufacturers_data_source, html_id='manufacturers_chart', options = { 'title': _('Manufacturer by Amount of WTG'), 'is3D': 'true', 'pieSliceText': 'label'})
	    context['manufacturers_chart'] = manufacturers_chart

	    country = queryset.values('wind_farm__country__name').annotate(wtgs=Count('wind_farm__country__name')).order_by('wtgs')
	    country_datalist = [[_('Country'), _('Amount WTG')]]
	    for wec in country:
	        temp = [wec['wind_farm__country__name'], wec['wtgs']]
	        country_datalist.append(temp)
	    country_data_source = SimpleDataSource(data=country_datalist)
	    country_chart = PieChart(country_data_source, html_id='country_chart', options = { 'title': _('Country by Amount of WTG'), 'is3D': 'true', 'pieSliceText': 'label'})
	    context['country_chart'] = country_chart

	    stat = queryset.values('status').annotate(wtgs=Count('status')).order_by('wtgs')
	    status_datalist = [[_('Status'), _('Amount WTG')]]
	    for wec in stat:
	        temp = [wec['status'], wec['wtgs']]
	        status_datalist.append(temp)
	    status_data_source = SimpleDataSource(data=status_datalist)
	    status_chart = PieChart(status_data_source, html_id='status_chart', options = { 'title': _('Status by Amount of WTG'), 'is3D': 'true', 'pieSliceText': 'label'})
	    context['status_chart'] = status_chart

	    offshore = queryset.values('offshore').annotate(wtgs=Count('offshore')).order_by('wtgs')
	    offshore_datalist = [['Offshore', _('Amount WTG')]]
	    for wec in offshore:
	        temp = [wec['offshore'], wec['wtgs']]
	        offshore_datalist.append(temp)
	    offshore_data_source = SimpleDataSource(data=offshore_datalist)
	    offshore_chart = PieChart(offshore_data_source, html_id='offshore_chart', options = { 'title': _('Offshore Status by Amount of WTG'), 'is3D': 'true', 'pieSliceText': 'label'})
	    context['offshore_chart'] = offshore_chart

	    year_data = {}
	    commisioning_years = [x for x in queryset.values_list('commisioning_year', flat=True) if x is not None]
	    for i in commisioning_years:
	        if i not in year_data.keys():
	            year_data[i] = 1
	        else:
	            year_data[i] += 1
	    year_datalist = [[_('Commisioning'), _('Amount WTG')]]
	    for key, value in sorted(year_data.items()):
	        temp = [str(key),value]
	        year_datalist.append(temp)
	    year_data_source = SimpleDataSource(data=year_datalist)
	    year_chart = BarChart(year_data_source, html_id='year_chart', options = { 'title': _('Commisioning by Amount of WTG'), 'is3D': 'true', 'colors': ['#092f57'], 'vAxis': { 'title': _('Year') }, 'hAxis': { 'title': _('Amount WTG') }})
	    context['year_chart'] = year_chart

	    return context

class ContractTableView(SingleTableView):
    filter_class = None
    context_filter_name = 'filter'

    def get_queryset(self, **kwargs):
        qs = super(ContractTableView, self).get_queryset().filter(active=True).prefetch_related('turbines', 'turbines__wind_farm', 'turbines__wec_typ', 'turbines__wec_typ__manufacturer').select_related('actor').annotate(first_commisioning=Case(When(turbines__commisioning_year__isnull=False, then=Min('turbines__commisioning_year'))))
        self.filter = self.filter_class(self.request.GET, queryset=qs)
        self.request.session['contract_json'] = serializers.serialize('json', self.filter.qs, fields=('pk'))
        return self.filter.qs

    def get_context_data(self, **kwargs):
	    context = super(ContractTableView, self).get_context_data()
	    context[self.context_filter_name] = self.filter

	    queryset = self.filter.qs

	    contracted_turbines = self.filter.qs.values_list('turbines__pk', flat=True)
	    turbines = Turbine.objects.filter(pk__in=contracted_turbines)

	    turbines_manufacturers = turbines.values_list('wec_typ__manufacturer__name', flat=True)
	    manufacturers_count = {}
	    for tm in turbines_manufacturers:
	        if tm not in manufacturers_count.keys():
	            manufacturers_count[tm] = 1
	        else:
	            manufacturers_count[tm] += 1
	    manufacturers_datalist = [[_('Manufacturer'), _('Amount WTG')]]
	    for m, count in manufacturers_count.items():
	        temp = [m, count]
	        manufacturers_datalist.append(temp)
	    manufacturers_data_source = SimpleDataSource(data=manufacturers_datalist)
	    manufacturers_chart = PieChart(manufacturers_data_source, html_id='manufacturers_chart', options = { 'title': _('Manufacturer by Amount of WTG'), 'is3D': 'true', 'pieSliceText': 'label'})
	    context['manufacturers_chart'] = manufacturers_chart

	    turbines_models = turbines.values_list('wec_typ__name', flat=True)
	    models_count = {}
	    for tm in turbines_models:
	        if tm not in models_count.keys():
	            models_count[tm] = 1
	        else:
	            models_count[tm] += 1
	    wec_type_datalist = [[_('WEC Type'), _('Amount WTG')]]
	    for m, count in models_count.items():
	        temp = [m, count]
	        wec_type_datalist.append(temp)
	    wec_type_data_source = SimpleDataSource(data=wec_type_datalist)
	    wec_type_chart = PieChart(wec_type_data_source, html_id='wec_type_chart', options = { 'title': _('Turbine Type by Amount of WTG'), 'is3D': 'true', 'pieSliceText': 'label'})
	    context['wec_type_chart'] = wec_type_chart

	    customer_turbine_count = {}
	    for c in queryset:
	        if c.actor.name not in customer_turbine_count.keys():
	            customer_turbine_count[c.actor.name] = c.amount_turbines
	        else:
	            customer_turbine_count[c.actor.name] += c.amount_turbines
	    customer_datalist = [[_('Customer'), _('Amount WTG')]]
	    for c, count in customer_turbine_count.items():
	        temp = [c, count]
	        customer_datalist.append(temp)
	    customer_data_source = SimpleDataSource(data=customer_datalist)
	    customer_chart = PieChart(customer_data_source, html_id='customer_chart', options = { 'title': _('Customer by Amount of WTG'), 'is3D': 'true', 'pieSliceText': 'label'})
	    context['customer_chart'] = customer_chart

	    age_data = {x : 0 for x in range(0,26)}
	    for i in queryset:
	        if type(i.turbine_age) == int:
	            age = i.turbine_age
	            if age >= 25:
	                age_data[25] += len(i.turbines.all())
	            else:
	                age_data[age] += len(i.turbines.all())
	        else:
	            pass
	    age_datalist = [[_('Age'), _('Amount WTG')]]
	    for key, value in sorted(age_data.items()):
	        temp = [str(key),value]
	        age_datalist.append(temp)
	    age_data_source = SimpleDataSource(data=age_datalist)
	    age_chart = BarChart(age_data_source, html_id='age_chart', options = { 'title': _('Age by Amount of WTG'), 'is3D': 'true', 'pieSliceText': 'label', 'colors': ['#092f57'], 'vAxis': { 'title': _('Age') }, 'hAxis': { 'title': _('Amount WTG') }})
	    context['age_chart'] = age_chart

	    country_turbine_count = {}
	    for c in queryset:
	        if c.contracted_country not in country_turbine_count.keys():
	            country_turbine_count[c.contracted_country] = c.amount_turbines
	        else:
	            country_turbine_count[c.contracted_country] += c.amount_turbines
	    country_datalist = [[_('Country'), _('Amount WTG')]]
	    for c, count in country_turbine_count.items():
	        temp = [c, count]
	        country_datalist.append(temp)
	    country_data_source = SimpleDataSource(data=country_datalist)
	    country_chart = PieChart(country_data_source, html_id='country_chart', options = { 'title': _('Country by Amount of WTG'), 'is3D': 'true', 'pieSliceText': 'label'})
	    context['country_chart'] = country_chart

	    service_locations = ServiceLocationSerializer(ServiceLocation.objects.filter(active=True).exclude(dwt="DWTS"), many=True).data
	    context["service_locations"] = service_locations
	    service_locations_dwts = ServiceLocationSerializer(ServiceLocation.objects.filter(active=True, dwt="DWTS"), many=True).data
	    context["service_locations_dwts"] = service_locations_dwts
	    return context

    @classmethod
    def generate_csv(cls, request):
        filename = "{}-contract-export.xls".format(datetime.now().replace(microsecond=0).isoformat())
        response = HttpResponse(content_type='applications/vnd.ms-excel')
        response['Content-Disposition'] = 'attachement; filename="{}"'.format(filename)
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet(_("Contract Overview"))
        row_num = 0
        columns = [(u'Einheit',5000), (u'Wind Farm', 5000), (u'Country', 5000), (u'Model', 5000), ('Amount', 3000), ('Contract Type', 5000), ('latitude', 4000), ('longitude', 4000), ('Commencement Date', 6000), ('Termination Date', 6000), ('Contractual Partner', 6000)]
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num][0], font_style)
            ws.col(col_num).width = columns[col_num][1]
        font_style = xlwt.XFStyle()
        font_style.alignment.wrap = 1
        deserialized = list(serializers.deserialize('json', request.session.get('contract_json')))
        pk_list = []
        for p in deserialized:
            pk_list.append(p.object.pk)
        queryset = Contract.objects.filter(pk__in=pk_list)
        for obj in queryset:
            row_num += 1
            row = [obj.dwt, obj.contracted_windfarm_name, obj.contracted_country, obj.contracted_wec_types_name, obj.amount_turbines, obj.contract_scope, obj.contract_coordinates['latitude'], obj.contract_coordinates['longitude'], obj.start_date, obj.end_date, obj.actor.name]
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)
        wb.save(response)
        return response

class ComponentTableView(SingleTableView):
    filter_class = None
    context_filter_name = 'filter'

    def get_queryset(self, **kwargs):
        qs = super(ComponentTableView, self).get_queryset()
        self.filter = self.filter_class(self.request.GET, queryset=qs)
        return self.filter.qs

    def get_context_data(self, **kwargs):
	    context = super(ComponentTableView, self).get_context_data()
	    context[self.context_filter_name] = self.filter
	    return context