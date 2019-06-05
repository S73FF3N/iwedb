from django_tables2 import SingleTableView
from graphos.sources.simple import SimpleDataSource
from graphos.renderers.gchart import PieChart, BarChart
from django.db.models import Min, Case, When
from django.http import HttpResponse
from django.core import serializers

import serpy
from datetime import datetime
import xlwt

from .admin import ProjectRessources
from .models import Project
from turbine.utils import ServiceLocationSerializer
from turbine.models import ServiceLocation
from turbine.utils import ContractSerializer
from turbine.models import Contract, Turbine

class ProjectSerializer(serpy.Serializer):
    pk = serpy.IntField()
    slug = serpy.Field()
    project_coordinates = serpy.Field()
    name = serpy.Field()
    amount_turbines = serpy.Field()
    project_wec_types_name = serpy.Field()

class ProjectSerializer2(serpy.Serializer):
    pk = serpy.IntField()

class PagedFilteredTableView(SingleTableView):
    filter_class = None
    context_filter_name = 'filter'

    def get_queryset(self,*args, **kwargs):
        qs = super(PagedFilteredTableView, self).get_queryset().filter(available=True).prefetch_related('turbines', 'turbines__wind_farm', 'turbines__wec_typ', 'turbines__wec_typ__manufacturer', 'turbines__wind_farm__country', 'turbines__owner', 'comment').select_related('customer', 'sales_manager').annotate(first_com_date=Case(When(turbines__commisioning_year__isnull=False, then=Min('turbines__commisioning_year')))).add_mw()
        self.filter = self.filter_class(self.request.GET, queryset=qs)
        self.request.session['search_queryset'] = serializers.serialize('json', self.filter.qs, fields=('pk'))
        return self.filter.qs

    def get_context_data(self, **kwargs):
	    context = super(PagedFilteredTableView, self).get_context_data()
	    context[self.context_filter_name] = self.filter
	    projects = ProjectSerializer(self.filter.qs, many=True).data
	    context["json"] = projects
	    service_locations_dwtx = ServiceLocationSerializer(ServiceLocation.objects.filter(active=True).exclude(dwt="DWTS"), many=True).data
	    context["service_locations"] = service_locations_dwtx
	    service_locations_dwts = ServiceLocationSerializer(ServiceLocation.objects.filter(active=True, dwt="DWTS"), many=True).data
	    context["service_locations_dwts"] = service_locations_dwts
	    contracts = ContractSerializer(Contract.objects.filter(active=True).prefetch_related('turbines', 'turbines__wind_farm'), many=True).data
	    context["contracts"] = contracts

	    queryset = self.filter.qs
	    age_data = {x : 0 for x in range(0,26)}
	    contracted_turbines = self.filter.qs.values_list('turbines__pk', flat=True)
	    turbines = Turbine.objects.filter(pk__in=contracted_turbines)

	    status_turbine_count = {}
	    for c in queryset:
	        if c.status not in status_turbine_count.keys():
	            status_turbine_count[c.status] = c.amount_turbines
	        else:
	            status_turbine_count[c.status] += c.amount_turbines
	    status_datalist = [['Customer', 'Amount WTG']]
	    for c, count in status_turbine_count.items():
	        temp = [c, count]
	        status_datalist.append(temp)
	    status_data_source = SimpleDataSource(data=status_datalist)
	    status_chart = PieChart(status_data_source, html_id='status_chart', options = { 'title': 'Status by Amount of WTG', 'is3D': 'true', 'pieSliceText': 'label'})
	    context['status_chart'] = status_chart

	    contract_type_turbine_count = {}
	    for c in queryset:
	        if c.contract_type not in contract_type_turbine_count.keys():
	            contract_type_turbine_count[c.contract_type] = c.amount_turbines
	        else:
	            contract_type_turbine_count[c.contract_type] += c.amount_turbines
	    contract_datalist = [['Customer', 'Amount WTG']]
	    for c, count in contract_type_turbine_count.items():
	        temp = [c, count]
	        contract_datalist.append(temp)
	    contract_data_source = SimpleDataSource(data=contract_datalist)
	    contract_chart = PieChart(contract_data_source, html_id='contract_chart', options = { 'title': 'Contract Type by Amount of WTG', 'is3D': 'true', 'pieSliceText': 'label'})
	    context['contract_chart'] = contract_chart

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
	        if c.customer.name not in customer_turbine_count.keys():
	            customer_turbine_count[c.customer.name] = c.amount_turbines
	        else:
	            customer_turbine_count[c.customer.name] += c.amount_turbines
	    customer_datalist = [['Customer', 'Amount WTG']]
	    for c, count in customer_turbine_count.items():
	        temp = [c, count]
	        customer_datalist.append(temp)
	    customer_data_source = SimpleDataSource(data=customer_datalist)
	    customer_chart = PieChart(customer_data_source, html_id='customer_chart', options = { 'title': 'Negotiation Partner by Amount of WTG', 'is3D': 'true', 'pieSliceText': 'label'})
	    context['customer_chart'] = customer_chart

	    for i in queryset:
	        if not i.start_operation is None:
	            start = i.start_operation.year
	        else:
	            start = datetime.now().year
	        if not i.first_com_date:
	            turbine_age = 'not defined'
	        else:
	            turbine_age = start - i.first_com_date
	            if turbine_age <= 0:
	                turbine_age = 0
	        if turbine_age != 'not defined' and turbine_age <= 25:
	            age_data[turbine_age] += i.turbines.all().count()
	        else:
	            pass
	    age_datalist = [['Age', 'Amount WTG']]
	    for key, value in sorted(age_data.items()):
	        temp = [str(key),value]
	        age_datalist.append(temp)
	    age_data_source = SimpleDataSource(data=age_datalist)
	    age_chart = BarChart(age_data_source, html_id='age_chart', options = { 'title': 'Age at contract commencement by Amount of WTG', 'is3D': 'true', 'pieSliceText': 'label', 'colors': ['#092f57'], 'vAxis': { 'title': 'Age' }, 'hAxis': { 'title': 'Amount WTG' }})
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
        columns = [(u'Einheit',5000), (u'Project', 5000), (u'Country', 5000), (u'Postal Code', 3000), (u'Negotiation Partner', 5000), (u'Phone', 3000), ('Contact Person', 5000), ('Mail', 7000), (u'Phone', 3000), ('Owner', 5000), ('OEM', 5000), ('WTG Type', 5000), ('Amount WTG', 5000), ('MW', 3000), ('Commisioning Date', 5000), ('Offer', 3000), ('Contract', 5000), ('Contract Type', 5000), ('Run Time', 3000), ('Price/WTG/a', 3000), ('Contract Value/a', 5000), ('Total Contract Value', 5000), ('EBT', 3000), ('First Contact', 3000), ('Contract Signature', 5000), ('Start Operations', 5000), ('Status', 5000), ('Probability', 5000), ('Sales Manager', 5000), ('Comments', 20000)]
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
            if obj.customer_contact == None:
                cust_cont_name = None
                cust_cont_mail = None
                cust_cont_phone = None
            else:
                cust_cont_name = obj.customer_contact.name
                cust_cont_mail = obj.customer_contact.mail
                cust_cont_phone = obj.customer_contact.phone.__str__()
            if obj.offer_number == None:
                of_nr = None
            else:
                of_nr = obj.offer_number.number
            row = [obj.dwt, obj.name, obj.project_country, obj.project_postal_codes, obj.customer.name, obj.customer.phone.__str__(), cust_cont_name, cust_cont_mail, cust_cont_phone, obj.project_owner_name, obj.project_oem_name, obj.project_wec_types_name, obj.amount_turbines, obj.mw, obj.first_commisioning, of_nr, obj.contract, obj.contract_type, obj.run_time, obj.price, obj.yearly_contract_value, obj.total_contract_value, obj.ebt, obj.request_date, obj.contract_signature, obj.start_operation, obj.status, obj.prob, obj.sales_manager.__str__(), obj.all_comments]
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)
        wb.save(response)
        return response

class PoolTableView(SingleTableView):
    filter_class = None
    context_filter_name = 'filter'

    def get_queryset(self,*args, **kwargs):
        qs = super(PoolTableView, self).get_queryset().filter(available=True).prefetch_related('projects', 'comment').select_related('customer', 'sales_manager')
        self.filter = self.filter_class(self.request.GET, queryset=qs)
        return self.filter.qs

    def get_context_data(self, **kwargs):
	    context = super(PoolTableView, self).get_context_data()
	    context[self.context_filter_name] = self.filter
	    return context