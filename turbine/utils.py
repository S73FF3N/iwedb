from django_tables2 import SingleTableView
from django.db.models import Count

import serpy
import operator
from graphos.sources.simple import SimpleDataSource
from graphos.renderers.gchart import PieChart, BarChart

from .models import ServiceLocation

class TurbineSerializer(serpy.Serializer):
    pk = serpy.IntField()
    slug = serpy.Field()
    latitude = serpy.Field()
    longitude = serpy.Field()
    turbine_id = serpy.Field()

class ContractSerializer(serpy.Serializer):
    pk = serpy.IntField()
    name = serpy.Field()
    wind_farm = serpy.MethodField()
    latitude = serpy.MethodField()
    longitude = serpy.MethodField()

    def  get_wind_farm(self, contract):
        wind_farm = contract.turbines.all()[0].wind_farm.name
        return wind_farm

    def get_longitude(self, contract):
        turbines = contract.turbines.all().filter(latitude__isnull=False, longitude__isnull=False)
        if not turbines:
            longitude = turbines[0].windfarm.longitude
        else:
            longitude = turbines[0].longitude
        return longitude

    def get_latitude(self, contract):
        turbines = contract.turbines.all().filter(latitude__isnull=False, longitude__isnull=False)
        if not turbines:
            latitude = turbines[0].windfarm.latitude
        else:
            latitude = turbines[0].latitude
        return latitude

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
        qs = super(PagedFilteredTableView, self).get_queryset().filter(available=True)
        self.filter = self.filter_class(self.request.GET, queryset=qs)
        return self.filter.qs

    def get_context_data(self, **kwargs):
	    context = super(PagedFilteredTableView, self).get_context_data()
	    context[self.context_filter_name] = self.filter
	    turbines_map = TurbineSerializer(self.filter.qs.filter(latitude__isnull=False, longitude__isnull=False), many=True).data
	    context["json"] = turbines_map

	    queryset = self.filter.qs

	    models = queryset.order_by().values_list('wec_typ__name', flat=True).distinct()
	    wec_type_data = {m : queryset.filter(wec_typ__name=m).aggregate(wtgs=Count('wec_typ')) for m in models}
	    wec_type_data = { key: value['wtgs'] for key, value in wec_type_data.items()}
	    wec_type_data = sorted(wec_type_data.items(), key=operator.itemgetter(1), reverse=True)
	    wec_type_datalist = [['WEC Type', 'Amount WTG']]
	    for wec in wec_type_data[:10]:
	        temp = [wec[0],wec[1]]
	        wec_type_datalist.append(temp)

	    manufacturers = queryset.order_by().values_list('wec_typ__manufacturer__name', flat=True).distinct()
	    manufacturers_data = {m : queryset.filter(wec_typ__manufacturer__name=m).aggregate(wtgs=Count('wec_typ')) for m in manufacturers}
	    manufacturers_data = { key: value['wtgs'] for key, value in manufacturers_data.items()}
	    manufacturers_data = sorted(manufacturers_data.items(), key=operator.itemgetter(1), reverse=True)
	    manufacturers_datalist = [['Manufacturer', 'Amount WTG']]
	    for wec in manufacturers_data[:10]:
	        temp = [wec[0],wec[1]]
	        manufacturers_datalist.append(temp)

	    country = queryset.order_by().values_list('wind_farm__country__name', flat=True).distinct()
	    country_data = {c : queryset.filter(wind_farm__country__name=c).aggregate(wtgs=Count('wec_typ')) for c in country}
	    country_datalist = [['Country', 'Amount WTG']]
	    for key, value in country_data.items():
	        temp = [key,value['wtgs']]
	        country_datalist.append(temp)

	    stat = queryset.order_by().values_list('status', flat=True).distinct()
	    status_data = {s : queryset.filter(status=s).aggregate(wtgs=Count('wec_typ')) for s in stat}
	    status_datalist = [['Status', 'Amount WTG']]
	    for key, value in status_data.items():
	        temp = [key,value['wtgs']]
	        status_datalist.append(temp)

	    offshore = queryset.order_by().values_list('offshore', flat=True).distinct()
	    offshore_data = {s : queryset.filter(offshore=s).aggregate(wtgs=Count('wec_typ')) for s in offshore}
	    offshore_datalist = [['Offshore', 'Amount WTG']]
	    for key, value in offshore_data.items():
	        temp = [key,value['wtgs']]
	        offshore_datalist.append(temp)

	    year_data = {}
	    for i in queryset:
	        try:
	            if i.yearpublished() not in year_data.keys():
	                year_data[i.yearpublished()] = 1
	            else:
	                year_data[i.yearpublished()] += 1
	        except:
	            pass
	    year_datalist = [['Commisioning', 'Amount WTG']]
	    for key, value in sorted(year_data.items()):
	        temp = [str(key),value]
	        year_datalist.append(temp)

	    wec_type_data_source = SimpleDataSource(data=wec_type_datalist)
	    wec_type_chart = PieChart(wec_type_data_source, html_id='wec_type_chart', options = { 'title': 'Turbine Type by Amount of WTG', 'is3D': 'true', 'pieSliceText': 'label'})
	    context['wec_type_chart'] = wec_type_chart

	    manufacturers_data_source = SimpleDataSource(data=manufacturers_datalist)
	    manufacturers_chart = PieChart(manufacturers_data_source, html_id='manufacturers_chart', options = { 'title': 'Manufacturer by Amount of WTG', 'is3D': 'true', 'pieSliceText': 'label'})
	    context['manufacturers_chart'] = manufacturers_chart

	    country_data_source = SimpleDataSource(data=country_datalist)
	    country_chart = PieChart(country_data_source, html_id='country_chart', options = { 'title': 'Country by Amount of WTG', 'is3D': 'true', 'pieSliceText': 'label'})
	    context['country_chart'] = country_chart

	    status_data_source = SimpleDataSource(data=status_datalist)
	    status_chart = PieChart(status_data_source, html_id='status_chart', options = { 'title': 'Status by Amount of WTG', 'is3D': 'true', 'pieSliceText': 'label'})
	    context['status_chart'] = status_chart

	    offshore_data_source = SimpleDataSource(data=offshore_datalist)
	    offshore_chart = PieChart(offshore_data_source, html_id='offshore_chart', options = { 'title': 'Offshore Status by Amount of WTG', 'is3D': 'true', 'pieSliceText': 'label'})
	    context['offshore_chart'] = offshore_chart

	    year_data_source = SimpleDataSource(data=year_datalist)
	    year_chart = BarChart(year_data_source, html_id='year_chart', options = { 'title': 'Commisioning by Amount of WTG', 'is3D': 'true', 'colors': ['#092f57'], 'vAxis': { 'title': 'Year' }, 'hAxis': { 'title': 'Amount WTG' }})
	    context['year_chart'] = year_chart

	    return context

class ContractTableView(SingleTableView):
    filter_class = None
    context_filter_name = 'filter'

    def get_queryset(self, **kwargs):
        qs = super(ContractTableView, self).get_queryset().filter(active=True)
        self.filter = self.filter_class(self.request.GET, queryset=qs)
        return self.filter.qs

    def get_context_data(self, **kwargs):
	    context = super(ContractTableView, self).get_context_data()
	    context[self.context_filter_name] = self.filter
	    contracts = ContractSerializer(self.filter.qs.filter(active=True), many=True).data

	    queryset = self.filter.qs

	    manufacturers = queryset.order_by().values_list('turbines__wec_typ__manufacturer__name', flat=True).distinct()
	    manufacturers_data = {m : queryset.filter(turbines__wec_typ__manufacturer__name=m).aggregate(wtgs=Count('turbines')) for m in manufacturers}
	    manufacturers_data = { key: value['wtgs'] for key, value in manufacturers_data.items()}
	    manufacturers_data = sorted(manufacturers_data.items(), key=operator.itemgetter(1), reverse=True)
	    manufacturers_datalist = [['Manufacturer', 'Amount WTG']]
	    for wec in manufacturers_data[:10]:
	        temp = [wec[0],wec[1]]
	        manufacturers_datalist.append(temp)
	    manufacturers_data_source = SimpleDataSource(data=manufacturers_datalist)
	    manufacturers_chart = PieChart(manufacturers_data_source, html_id='manufacturers_chart', options = { 'title': 'Manufacturer by Amount of WTG', 'is3D': 'true', 'pieSliceText': 'label'})
	    context['manufacturers_chart'] = manufacturers_chart

	    models = queryset.order_by().values_list('turbines__wec_typ__name', flat=True).distinct()
	    wec_type_data = {m : queryset.filter(turbines__wec_typ__name=m).aggregate(wtgs=Count('turbines')) for m in models}
	    wec_type_data = { key: value['wtgs'] for key, value in wec_type_data.items()}
	    wec_type_data = sorted(wec_type_data.items(), key=operator.itemgetter(1), reverse=True)
	    wec_type_datalist = [['WEC Type', 'Amount WTG']]
	    for wec in wec_type_data[:10]:
	        temp = [wec[0],wec[1]]
	        wec_type_datalist.append(temp)
	    wec_type_data_source = SimpleDataSource(data=wec_type_datalist)
	    wec_type_chart = PieChart(wec_type_data_source, html_id='wec_type_chart', options = { 'title': 'WEC Type by Amount of WTG', 'is3D': 'true', 'pieSliceText': 'label'})
	    context['wec_type_chart'] = wec_type_chart

	    customers = queryset.order_by().values_list('actor__name', flat=True).distinct()
	    customer_data = { c: queryset.filter(actor__name=c).aggregate(wtgs=Count('turbines')) for c in customers}
	    customer_data = { key: value['wtgs'] for key, value in customer_data.items()}
	    customer_data = sorted(customer_data.items(), key=operator.itemgetter(1), reverse=True)
	    customer_datalist = [['Customer', 'Amount WTG']]
	    for c in customer_data[:10]:
	        temp = [c[0],c[1]]
	        customer_datalist.append(temp)
	    customer_data_source = SimpleDataSource(data=customer_datalist)
	    customer_chart = PieChart(customer_data_source, html_id='customer_chart', options = { 'title': 'Customer by Amount of WTG', 'is3D': 'true', 'pieSliceText': 'label'})
	    context['customer_chart'] = customer_chart

	    age_data = {x : 0 for x in range(0,21)}
	    for i in queryset:
	        if i.turbine_age() != 'not defined':
	            age = i.turbine_age()
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

	    country = queryset.order_by().values_list('turbines__wind_farm__country__name', flat=True).distinct()
	    country_data = {c : queryset.filter(turbines__wind_farm__country__name=c).aggregate(wtgs=Count('turbines')) for c in country}
	    country_datalist = [['Country', 'Amount WTG']]
	    for key, value in country_data.items():
	        temp = [key,value['wtgs']]
	        country_datalist.append(temp)
	    country_data_source = SimpleDataSource(data=country_datalist)
	    country_chart = PieChart(country_data_source, html_id='country_chart', options = { 'title': 'Country by Amount of WTG', 'is3D': 'true', 'pieSliceText': 'label'})
	    context['country_chart'] = country_chart

	    context["json"] = contracts
	    service_locations = ServiceLocationSerializer(ServiceLocation.objects.filter(active=True, dwt="DWTX"), many=True).data
	    context["service_locations"] = service_locations
	    service_locations_dwts = ServiceLocationSerializer(ServiceLocation.objects.filter(active=True, dwt="DWTS"), many=True).data
	    context["service_locations_dwts"] = service_locations_dwts
	    return context