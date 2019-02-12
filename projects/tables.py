from django.contrib.humanize.templatetags.humanize import intcomma

import django_tables2 as dt2

from .models import Project, Calculation_Tool, OfferNumber

class ProjectTable(dt2.Table):
    name = dt2.LinkColumn(None, footer='Total')
    amount_turbines = dt2.Column(verbose_name='Turbines', footer=lambda table: sum(x.amount_turbines for x in table.data), orderable=False)
    project_oem_name = dt2.Column(verbose_name='OEM', orderable=False)
    project_wec_types_name = dt2.Column(verbose_name='Model', orderable=False)
    project_country = dt2.Column(verbose_name='Country')
    offer_nr = dt2.Column(verbose_name="Offer")
    prob = dt2.Column(verbose_name="%")

    class Meta:
        model = Project
        fields =('name', 'status', 'prob', 'project_oem_name', 'project_wec_types_name', 'amount_turbines', 'start_operation', 'project_country', 'customer', 'offer_nr', 'contract_type')#'last_update', 'contract_signature','mw',
        attrs = {"class": "windfarms"}
        per_page = 20
        empty_text = "There are no projects matching the search criteria..."

class OfferNumberTable(dt2.Table):
    class Meta:
        model = OfferNumber
        fields = ('number', 'wind_farm', 'amount', 'wec_typ', 'sales_manager', 'text')
        attrs = {"class": "windfarms"}
        per_page = 20
        empty_text = "There are no offer numbers matching the search criteria..."

class Calculation_ToolTable(dt2.Table):
    country_names = dt2.Column(verbose_name="Country", orderable=False)

    class Meta:
        model = Calculation_Tool
        fields = ('file', 'version', 'country_names', 'created')
        attrs = {"class": "windfarms"}
        per_page = 20
        empty_text = "There are no calculation tools matching the search criteria..."

class TotalVolumeTable(dt2.Table):
    name = dt2.LinkColumn(None, footer='Total')
    amount_turbines = dt2.Column(verbose_name='Turbines', footer=lambda table: sum(x.amount_turbines for x in table.data), orderable=False)
    project_oem_name = dt2.Column(verbose_name='OEM', orderable=False)
    project_wec_types_name = dt2.Column(verbose_name='Model', orderable=False)
    mw = dt2.Column(verbose_name='Power [MW]', orderable=False)#, footer=lambda table: sum(x.mw for x in table.data)
    project_country = dt2.Column(verbose_name='Country')
    dwt = dt2.Column(verbose_name="DWT")
    start_operation = dt2.DateColumn(format='d b Y')
    total_contract_value = dt2.Column(footer=lambda table: sum(x.total_contract_value for x in table.data), verbose_name="Total Contract Value [€]", orderable=False)
    yearly_contract_value = dt2.Column(footer=lambda table: sum(x.yearly_contract_value for x in table.data), verbose_name="Yearly Contract Value [€/a]", orderable=False)

    class Meta:
        model = Project
        fields =('name', 'status', 'project_oem_name', 'project_wec_types_name', 'amount_turbines', 'mw', 'start_operation', 'dwt', 'project_country', 'yearly_contract_value', 'total_contract_value')
        attrs = {"class": "windfarms"}
        per_page = 20
        empty_text = "There are no projects matching the search criteria..."

    def render_total_contract_value(self, value):
        return intcomma(value)

    def render_yearly_contract_value(self, value):
        return intcomma(value)

class NewEntriesTable(dt2.Table):
    name = dt2.LinkColumn(None, footer='Total')
    amount_turbines = dt2.Column(verbose_name='Turbines', footer=lambda table: sum(x.amount_turbines for x in table.data), orderable=False)
    project_oem_name = dt2.Column(verbose_name='OEM', orderable=False)
    project_wec_types_name = dt2.Column(verbose_name='Model', orderable=False)
    mw = dt2.Column(verbose_name='Power [MW]', orderable=False)#footer=lambda table: sum(x.mw for x in table.data)
    project_country = dt2.Column(verbose_name='Country')
    dwt = dt2.Column(verbose_name="DWT")
    start_operation = dt2.DateColumn(format='d b Y')
    request_date = dt2.Column(verbose_name='First Contract')

    class Meta:
        model = Project
        fields =('name', 'status', 'project_oem_name', 'project_wec_types_name', 'amount_turbines', 'mw', 'start_operation', 'request_date', 'dwt', 'project_country', 'customer')
        attrs = {"class": "windfarms"}
        per_page = 20
        empty_text = "There are no projects matching the search criteria..."
