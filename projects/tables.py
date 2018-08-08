import django_tables2 as dt2
from .models import Project

class ProjectTable(dt2.Table):
    name = dt2.LinkColumn(None)
    amount_turbines = dt2.Column(accessor='amount_turbines', verbose_name='Turbines', orderable=False)
    project_windfarm = dt2.Column(accessor='project_windfarm_name', verbose_name='Wind Farm', orderable=False)
    project_oems = dt2.Column(accessor='project_oem_name', verbose_name='OEM', orderable=False)
    project_wec_types = dt2.Column(accessor='project_wec_types_name', verbose_name='Model', orderable=False)
    #mw = dt2.Column(accessor='mw', verbose_name='Power [MW]', orderable=False)
    #turbine_age = dt2.Column(accessor='turbine_age', verbose_name='Age [years]', orderable=False)
    project_country = dt2.Column(accessor='project_country', verbose_name='Country', orderable=False)
    #project_owner = dt2.Column(accessor='project_owner_name', verbose_name='Owner', orderable=False)
    #dwt = dt2.Column(verbose_name="DWT")

    class Meta:
        model = Project
        fields =('name', 'project_windfarm', 'status', 'project_oems', 'project_wec_types', 'amount_turbines', 'start_operation', 'last_contact', 'project_country', 'customer')#'prob', 'dwt', 'mw', 'turbine_age', 'project_owner',
        attrs = {"class": "windfarms"}
        per_page = 20
        empty_text = "There are no projects matching the search criteria..."