from django_tables2 import SingleTableView
from graphos.sources.simple import SimpleDataSource
from graphos.renderers.gchart import PieChart, BarChart
from django.db.models import Count

import operator
import serpy

from turbine.utils import ServiceLocationSerializer
from turbine.models import ServiceLocation
from turbine.utils import ContractSerializer
from turbine.models import Contract

class ProjectSerializer(serpy.Serializer):
    pk = serpy.IntField()
    slug = serpy.Field()
    latitude = serpy.MethodField()
    longitude = serpy.MethodField()
    name = serpy.Field()

    def get_longitude(self, project):
        turbines = project.turbines.all().filter(latitude__isnull=False, longitude__isnull=False)
        if not turbines:
            try:
                longitude = turbines[0].windfarm.longitude
            except:
                longitude = 49.8046937
        else:
            longitude = turbines[0].longitude
        return longitude

    def get_latitude(self, project):
        turbines = project.turbines.all().filter(latitude__isnull=False, longitude__isnull=False)
        if not turbines:
            try:
                latitude = turbines[0].windfarm.latitude
            except:
                latitude = 1.8066702
        else:
            latitude = turbines[0].latitude
        return latitude

class PagedFilteredTableView(SingleTableView):
    filter_class = None
    context_filter_name = 'filter'

    def get_queryset(self,*args, **kwargs):
        qs = super(PagedFilteredTableView, self).get_queryset().filter(available=True)
        self.filter = self.filter_class(self.request.GET, queryset=qs)
        return self.filter.qs

    def get_context_data(self, **kwargs):
	    context = super(PagedFilteredTableView, self).get_context_data()
	    context[self.context_filter_name] = self.filter
	    projects = ProjectSerializer(self.filter.qs.filter(status__in=['Coffee', 'Soft Offer', 'Hard Offer', 'Negotiation', 'Final Negotiation']), many=True).data
	    context["json"] = projects
	    service_locations = ServiceLocationSerializer(ServiceLocation.objects.filter(active=True), many=True).data
	    context["service_locations"] = service_locations
	    contracts = ContractSerializer(Contract.objects.filter(active=True), many=True).data
	    context["contracts"] = contracts

	    queryset = self.filter.qs
	    context['projects'] = queryset
	    age_data = {x : 0 for x in range(0,21)}
	    stat = queryset.order_by().values_list('status', flat=True).distinct()
	    status_data = {s : queryset.filter(status=s).aggregate(wtgs=Count('turbines')) for s in stat}
	    status_datalist = [['Status', 'Amount WTG']]
	    for key, value in status_data.items():
	        temp = [key,value['wtgs']]
	        status_datalist.append(temp)
	    department = queryset.order_by().values_list('department', flat=True).distinct()
	    department_data = {d : queryset.filter(department=d).aggregate(wtgs=Count('turbines')) for d in department}
	    department_datalist = [['Department', 'Amount WTG']]
	    for key, value in department_data.items():
	        temp = [key,value['wtgs']]
	        department_datalist.append(temp)
	    contract = queryset.order_by().values_list('contract_type', flat=True).distinct()
	    contract_data = {c : queryset.filter(contract_type=c).aggregate(wtgs=Count('turbines')) for c in contract}
	    contract_datalist = [['Contract Type', 'Amount WTG']]
	    for key, value in contract_data.items():
	        temp = [key,value['wtgs']]
	        contract_datalist.append(temp)
	    models = queryset.order_by().values_list('turbines__wec_typ__name', flat=True).distinct()
	    wec_type_data = {m : queryset.filter(turbines__wec_typ__name=m).aggregate(wtgs=Count('turbines')) for m in models}
	    wec_type_data = { key: value['wtgs'] for key, value in wec_type_data.items()}
	    wec_type_data = sorted(wec_type_data.items(), key=operator.itemgetter(1), reverse=True)
	    wec_type_datalist = [['WEC Type', 'Amount WTG']]
	    for wec in wec_type_data[:10]:
	        temp = [wec[0],wec[1]]
	        wec_type_datalist.append(temp)
	    customers = queryset.order_by().values_list('customer__name', flat=True).distinct()
	    customer_data = { c: queryset.filter(customer__name=c).aggregate(wtgs=Count('turbines')) for c in customers}
	    customer_data = { key: value['wtgs'] for key, value in customer_data.items()}
	    customer_data = sorted(customer_data.items(), key=operator.itemgetter(1), reverse=True)
	    customer_datalist = [['Customer', 'Amount WTG']]
	    for c in customer_data[:10]:
	        temp = [c[0],c[1]]
	        customer_datalist.append(temp)
	    for i in queryset:
	        age = i.turbine_age()
	        age_data[age] += len(i.turbines.all())
	    age_datalist = [['Age', 'Amount WTG']]
	    for key, value in sorted(age_data.items()):
	        temp = [str(key),value]
	        age_datalist.append(temp)
	    status_data_source = SimpleDataSource(data=status_datalist)
	    status_chart = PieChart(status_data_source, html_id='status_chart', options = { 'title': 'Status by Amount of WTG', 'is3D': 'true', 'pieSliceText': 'label'})
	    context['status_chart'] = status_chart
	    department_data_source = SimpleDataSource(data=department_datalist)
	    department_chart = PieChart(department_data_source, html_id='department_chart', options = { 'title': 'Department by Amount of WTG', 'is3D': 'true', 'pieSliceText': 'label'})
	    context['department_chart'] = department_chart
	    contract_data_source = SimpleDataSource(data=contract_datalist)
	    contract_chart = PieChart(contract_data_source, html_id='contract_chart', options = { 'title': 'Contract Type by Amount of WTG', 'is3D': 'true', 'pieSliceText': 'label'})
	    context['contract_chart'] = contract_chart
	    wec_type_data_source = SimpleDataSource(data=wec_type_datalist)
	    wec_type_chart = PieChart(wec_type_data_source, html_id='wec_type_chart', options = { 'title': 'WEC Type by Amount of WTG', 'is3D': 'true', 'pieSliceText': 'label'})
	    context['wec_type_chart'] = wec_type_chart
	    customer_data_source = SimpleDataSource(data=customer_datalist)
	    customer_chart = PieChart(customer_data_source, html_id='customer_chart', options = { 'title': 'Customer by Amount of WTG', 'is3D': 'true', 'pieSliceText': 'label'})
	    context['customer_chart'] = customer_chart
	    age_data_source = SimpleDataSource(data=age_datalist)
	    age_chart = BarChart(age_data_source, html_id='age_chart', options = { 'title': 'Age by Amount of WTG', 'is3D': 'true', 'pieSliceText': 'label', 'colors': ['#092f57'], 'vAxis': { 'title': 'Age' }, 'hAxis': { 'title': 'Amount WTG' }})
	    context['age_chart'] = age_chart
	    return context