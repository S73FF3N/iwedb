from django_tables2 import SingleTableView
from graphos.sources.simple import SimpleDataSource
from graphos.renderers.gchart import PieChart, BarChart
from django.db.models import Count
from django.http import HttpResponse
from django.core import serializers

import operator
import serpy
from datetime import datetime
import xlwt

from .admin import ProjectRessources
from .models import Project
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
                if project.turbines.all()[0].wind_farm.longitude != None:
                    longitude = project.turbines.all()[0].wind_farm.longitude
                else:
                    longitude = 49.8046937
            except:
                longitude = 49.8046937
        else:
            longitude = turbines[0].longitude
        return longitude

    def get_latitude(self, project):
        turbines = project.turbines.all().filter(latitude__isnull=False, longitude__isnull=False)
        if not turbines:
            try:
                if project.turbines.all()[0].wind_farm.latitude != None:
                    latitude = project.turbines.all()[0].wind_farm.latitude
                else:
                    latitude = 1.8066702
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
        self.request.session['search_queryset'] = serializers.serialize('json', self.filter.qs)
        return self.filter.qs

    def get_context_data(self, **kwargs):
	    context = super(PagedFilteredTableView, self).get_context_data()
	    context[self.context_filter_name] = self.filter
	    projects = ProjectSerializer(self.filter.qs, many=True).data
	    context["json"] = projects
	    service_locations_dwtx = ServiceLocationSerializer(ServiceLocation.objects.filter(active=True, dwt="DWTX"), many=True).data
	    context["service_locations"] = service_locations_dwtx
	    service_locations_dwts = ServiceLocationSerializer(ServiceLocation.objects.filter(active=True, dwt="DWTS"), many=True).data
	    context["service_locations_dwts"] = service_locations_dwts
	    contracts = ContractSerializer(Contract.objects.filter(active=True), many=True).data
	    context["contracts"] = contracts

	    queryset = self.filter.qs
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
	        if i.turbine_age() != 'not defined':
	            age = i.turbine_age()
	            age_data[age] += len(i.turbines.all())
	        else:
	            pass
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
	    wec_type_chart = PieChart(wec_type_data_source, html_id='wec_type_chart', options = { 'title': 'Turbine Type by Amount of WTG', 'is3D': 'true', 'pieSliceText': 'label'})
	    context['wec_type_chart'] = wec_type_chart
	    customer_data_source = SimpleDataSource(data=customer_datalist)
	    customer_chart = PieChart(customer_data_source, html_id='customer_chart', options = { 'title': 'Customer by Amount of WTG', 'is3D': 'true', 'pieSliceText': 'label'})
	    context['customer_chart'] = customer_chart
	    age_data_source = SimpleDataSource(data=age_datalist)
	    age_chart = BarChart(age_data_source, html_id='age_chart', options = { 'title': 'Age by Amount of WTG', 'is3D': 'true', 'pieSliceText': 'label', 'colors': ['#092f57'], 'vAxis': { 'title': 'Age' }, 'hAxis': { 'title': 'Amount WTG' }})
	    context['age_chart'] = age_chart
	    return context

    def export_xlsx(request):
        queryset = Project.objects.exclude(status='Potential')
        data = ProjectRessources().export(queryset)
        response = HttpResponse(data.xlsx, content_type='applications/vnd.ms-excel')
        response['Content-Disposition'] = 'attachement; filename="projects.xlsx"'
        return response

    @classmethod
    def generate_csv(cls, request):
        filename = "{}-export.xls".format(datetime.now().replace(microsecond=0).isoformat())
        response = HttpResponse(content_type='applications/vnd.ms-excel')
        response['Content-Disposition'] = 'attachement; filename="{}"'.format(filename)
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet("Project Overview")
        row_num = 0
        columns = [(u'Einheit',5000), (u'Project', 5000), (u'Country', 5000), (u'Customer', 5000), ('Operator', 5000), ('OEM', 5000), ('WTG Type', 5000), ('Amount WTG', 5000), ('Commisioning Date', 5000), ('Contract Type', 5000), ('Run Time', 3000), ('Price/WTG/a', 3000), ('Contract Value/a', 5000), ('EBT', 3000), ('Contract Signature', 5000), ('Start Operations', 5000), ('Status', 5000), ('Probability', 5000), ('Sales Manager', 5000), ('Comments', 20000)]
        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num][0], font_style)
            ws.col(col_num).width = columns[col_num][1]
        font_style = xlwt.XFStyle()
        font_style.alignment.wrap = 1
        deserialized = list(serializers.deserialize('json', request.session.get('search_queryset')))
        pk_list = []
        for p in deserialized:
            pk_list.append(p.object.pk)
        queryset = Project.objects.filter(pk__in=pk_list)
        for obj in queryset:
            row_num += 1
            row = [obj.dwt, obj.name, obj.project_country(), obj.customer.name, obj.project_owner_name(), obj.project_oem_name(), obj.project_wec_types_name(), obj.amount_turbines(), obj.first_commisioning(), obj.contract_type, obj.run_time, obj.price, obj.yearly_contract_value(), obj.ebt, obj.contract_signature, obj.start_operation, obj.status, obj.prob, obj.responsible, obj.all_comments()]
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)
        wb.save(response)
        return response
