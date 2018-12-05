from django_tables2 import SingleTableView
from django.db.models import Count, Min, Case, When

import serpy
from graphos.sources.simple import SimpleDataSource
from graphos.renderers.gchart import PieChart, BarChart

from .models import ServiceLocation, Turbine

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
    location_type = serpy.Field()
    latitude = serpy.Field()
    longitude = serpy.Field()

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
	    turbines_map = TurbineSerializer(self.filter.qs.filter(latitude__isnull=False, longitude__isnull=False), many=True).data
	    context["json"] = turbines_map

	    queryset = self.filter.qs

	    models = queryset.values('wec_typ__name').annotate(wtgs=Count('wec_typ__name')).order_by('-wtgs')
	    wec_type_datalist = [['WEC Type', 'Amount WTG']]
	    for wec in models[:10]:
	        temp = [wec['wec_typ__name'], wec['wtgs']]
	        wec_type_datalist.append(temp)
	    wec_type_data_source = SimpleDataSource(data=wec_type_datalist)
	    wec_type_chart = PieChart(wec_type_data_source, html_id='wec_type_chart', options = { 'title': 'Turbine Type by Amount of WTG', 'is3D': 'true', 'pieSliceText': 'label'})
	    context['wec_type_chart'] = wec_type_chart

	    manufacturers = queryset.values('wec_typ__manufacturer__name').annotate(wtgs=Count('wec_typ__manufacturer__name')).order_by('-wtgs')
	    manufacturers_datalist = [['Manufacturer', 'Amount WTG']]
	    for wec in manufacturers[:10]:
	        temp = [wec['wec_typ__manufacturer__name'], wec['wtgs']]
	        manufacturers_datalist.append(temp)
	    manufacturers_data_source = SimpleDataSource(data=manufacturers_datalist)
	    manufacturers_chart = PieChart(manufacturers_data_source, html_id='manufacturers_chart', options = { 'title': 'Manufacturer by Amount of WTG', 'is3D': 'true', 'pieSliceText': 'label'})
	    context['manufacturers_chart'] = manufacturers_chart

	    country = queryset.values('wind_farm__country__name').annotate(wtgs=Count('wind_farm__country__name')).order_by('wtgs')
	    country_datalist = [['Country', 'Amount WTG']]
	    for wec in country:
	        temp = [wec['wind_farm__country__name'], wec['wtgs']]
	        country_datalist.append(temp)
	    country_data_source = SimpleDataSource(data=country_datalist)
	    country_chart = PieChart(country_data_source, html_id='country_chart', options = { 'title': 'Country by Amount of WTG', 'is3D': 'true', 'pieSliceText': 'label'})
	    context['country_chart'] = country_chart

	    stat = queryset.values('status').annotate(wtgs=Count('status')).order_by('wtgs')
	    status_datalist = [['Status', 'Amount WTG']]
	    for wec in stat:
	        temp = [wec['status'], wec['wtgs']]
	        status_datalist.append(temp)
	    status_data_source = SimpleDataSource(data=status_datalist)
	    status_chart = PieChart(status_data_source, html_id='status_chart', options = { 'title': 'Status by Amount of WTG', 'is3D': 'true', 'pieSliceText': 'label'})
	    context['status_chart'] = status_chart

	    offshore = queryset.values('offshore').annotate(wtgs=Count('offshore')).order_by('wtgs')
	    offshore_datalist = [['Offshore', 'Amount WTG']]
	    for wec in offshore:
	        temp = [wec['offshore'], wec['wtgs']]
	        offshore_datalist.append(temp)
	    offshore_data_source = SimpleDataSource(data=offshore_datalist)
	    offshore_chart = PieChart(offshore_data_source, html_id='offshore_chart', options = { 'title': 'Offshore Status by Amount of WTG', 'is3D': 'true', 'pieSliceText': 'label'})
	    context['offshore_chart'] = offshore_chart

	    year_data = {}
	    commisioning_years = [x for x in queryset.values_list('commisioning', flat=True) if x is not None]
	    for i in commisioning_years:
	        if i.strftime('%Y') not in year_data.keys():
	            year_data[i.strftime('%Y')] = 1
	        else:
	            year_data[i.strftime('%Y')] += 1
	    year_datalist = [['Commisioning', 'Amount WTG']]
	    for key, value in sorted(year_data.items()):
	        temp = [str(key),value]
	        year_datalist.append(temp)
	    year_data_source = SimpleDataSource(data=year_datalist)
	    year_chart = BarChart(year_data_source, html_id='year_chart', options = { 'title': 'Commisioning by Amount of WTG', 'is3D': 'true', 'colors': ['#092f57'], 'vAxis': { 'title': 'Year' }, 'hAxis': { 'title': 'Amount WTG' }})
	    context['year_chart'] = year_chart

	    return context

class ContractTableView(SingleTableView):
    filter_class = None
    context_filter_name = 'filter'

    def get_queryset(self, **kwargs):
        qs = super(ContractTableView, self).get_queryset().filter(active=True).prefetch_related('turbines', 'turbines__wind_farm', 'turbines__wec_typ', 'turbines__wec_typ__manufacturer').select_related('actor').annotate(first_commisioning=Case(When(turbines__commisioning__isnull=False, then=Min('turbines__commisioning'))))
        self.filter = self.filter_class(self.request.GET, queryset=qs)
        return self.filter.qs

    def get_context_data(self, **kwargs):
	    context = super(ContractTableView, self).get_context_data()
	    context[self.context_filter_name] = self.filter
	    contracts = ContractSerializer(self.filter.qs, many=True).data
	    context["json"] = contracts

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
	    manufacturers_datalist = [['Manufacturer', 'Amount WTG']]
	    for m, count in manufacturers_count.items():
	        temp = [m, count]
	        manufacturers_datalist.append(temp)
	    manufacturers_data_source = SimpleDataSource(data=manufacturers_datalist)
	    manufacturers_chart = PieChart(manufacturers_data_source, html_id='manufacturers_chart', options = { 'title': 'Manufacturer by Amount of WTG', 'is3D': 'true', 'pieSliceText': 'label'})
	    context['manufacturers_chart'] = manufacturers_chart

	    turbines_models = turbines.values_list('wec_typ__name', flat=True)
	    models_count = {}
	    for tm in turbines_models:
	        if tm not in models_count.keys():
	            models_count[tm] = 1
	        else:
	            models_count[tm] += 1
	    wec_type_datalist = [['WEC Type', 'Amount WTG']]
	    for m, count in models_count.items():
	        temp = [m, count]
	        wec_type_datalist.append(temp)
	    wec_type_data_source = SimpleDataSource(data=wec_type_datalist)
	    wec_type_chart = PieChart(wec_type_data_source, html_id='wec_type_chart', options = { 'title': 'Turbine Type by Amount of WTG', 'is3D': 'true', 'pieSliceText': 'label'})
	    context['wec_type_chart'] = wec_type_chart

	    customer_turbine_count = {}
	    for c in queryset:
	        if c.actor.name not in customer_turbine_count.keys():
	            customer_turbine_count[c.actor.name] = c.amount_turbines
	        else:
	            customer_turbine_count[c.actor.name] += c.amount_turbines
	    customer_datalist = [['Customer', 'Amount WTG']]
	    for c, count in customer_turbine_count.items():
	        temp = [c, count]
	        customer_datalist.append(temp)
	    customer_data_source = SimpleDataSource(data=customer_datalist)
	    customer_chart = PieChart(customer_data_source, html_id='customer_chart', options = { 'title': 'Customer by Amount of WTG', 'is3D': 'true', 'pieSliceText': 'label'})
	    context['customer_chart'] = customer_chart

	    age_data = {x : 0 for x in range(0,26)}
	    for i in queryset:
	        if i.turbine_age != 'not defined':
	            age = i.turbine_age
	            age_data[age] += len(i.turbines.all())
	        else:
	            pass
	    age_datalist = [['Age', 'Amount WTG']]
	    for key, value in sorted(age_data.items()):
	        temp = [str(key),value]
	        age_datalist.append(temp)
	    age_data_source = SimpleDataSource(data=age_datalist)
	    age_chart = BarChart(age_data_source, html_id='age_chart', options = { 'title': 'Age by Amount of WTG', 'is3D': 'true', 'pieSliceText': 'label', 'colors': ['#092f57'], 'vAxis': { 'title': 'Age' }, 'hAxis': { 'title': 'Amount WTG' }})
	    context['age_chart'] = age_chart

	    country_turbine_count = {}
	    for c in queryset:
	        if c.contracted_country not in country_turbine_count.keys():
	            country_turbine_count[c.contracted_country] = c.amount_turbines
	        else:
	            country_turbine_count[c.contracted_country] += c.amount_turbines
	    country_datalist = [['Country', 'Amount WTG']]
	    for c, count in country_turbine_count.items():
	        temp = [c, count]
	        country_datalist.append(temp)
	    country_data_source = SimpleDataSource(data=country_datalist)
	    country_chart = PieChart(country_data_source, html_id='country_chart', options = { 'title': 'Country by Amount of WTG', 'is3D': 'true', 'pieSliceText': 'label'})
	    context['country_chart'] = country_chart

	    service_locations = ServiceLocationSerializer(ServiceLocation.objects.filter(active=True).exclude(dwt="DWTS"), many=True).data
	    context["service_locations"] = service_locations
	    service_locations_dwts = ServiceLocationSerializer(ServiceLocation.objects.filter(active=True, dwt="DWTS"), many=True).data
	    context["service_locations_dwts"] = service_locations_dwts
	    return context