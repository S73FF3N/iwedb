import django_tables2 as dt2
from django.utils.translation import ugettext_lazy as _

from .models import Turbine, Contract, Component

class TurbineTable(dt2.Table):
    turbine_id = dt2.LinkColumn(None)

    class Meta:
        model = Turbine
        fields =('turbine_id', 'wind_farm', 'wec_typ', 'status')
        attrs = {"class": "windfarms"}
        per_page = 25
        empty_text = _("There are no turbines matching the search criteria...")

class ContractTable(dt2.Table):
    amount_turbines = dt2.Column(verbose_name=_('Amount'), footer=lambda table: sum(x.amount_turbines for x in table.data), orderable=False)
    contracted_windfarm = dt2.Column(accessor='contracted_windfarm_name', verbose_name=_('Wind Farm'), orderable=False)
    manufacturer = dt2.Column(accessor='contracted_oem_name', verbose_name=_('Manufacturer'), orderable=False)
    wec_type = dt2.Column(accessor='contracted_wec_types_name', verbose_name='Model', orderable=False)
    name = dt2.LinkColumn(None, footer='Total')
    start_date = dt2.DateColumn(format='d b Y')
    end_date = dt2.DateColumn(format='d b Y')
    actor = dt2.Column(verbose_name=_('Contractual Partner'))
    contract_scope = dt2.Column(accessor='contract_scope', verbose_name=_('Contract Type'), orderable=False)

    class Meta:
        model = Contract
        fields =('name', 'contracted_windfarm', 'dwt', 'contract_scope', 'amount_turbines', 'manufacturer', 'wec_type', 'actor', 'start_date', 'end_date')
        attrs = {"class": "windfarms"}
        per_page = 25
        empty_text = _("There are no contracts matching the search criteria...")

class ComponentTable(dt2.Table):
    component_name = dt2.LinkColumn(None, verbose_name=_("Component"))

    class Meta:
        model = Component
        fields = ('component_name', 'component_manufacturer', 'component_type')
        attrs = {"class": "windfarms"}
        per_page = 25
        empty_text = _("There are no components matching the search criteria")

class TerminatedContractTable(dt2.Table):
    amount_turbines = dt2.Column(verbose_name=_('Amount'), footer=lambda table: sum(x.amount_turbines for x in table.data), orderable=False)
    contracted_windfarm = dt2.Column(accessor='contracted_windfarm_name', verbose_name=_('Wind Farm'), orderable=False)
    manufacturer = dt2.Column(accessor='contracted_oem_name', verbose_name=_('Manufacturer'), orderable=False)
    wec_type = dt2.Column(accessor='contracted_wec_types_name', verbose_name='Model', orderable=False)
    name = dt2.LinkColumn(None, footer='Total')
    start_date = dt2.DateColumn(format='d b Y')
    end_date = dt2.DateColumn(format='d b Y')
    actor = dt2.Column(verbose_name=_('Contractual Partner'))
    contract_scope = dt2.Column(accessor='contract_scope', verbose_name=_('Contract Type'), orderable=False)

    class Meta:
        model = Contract
        fields =('name', 'contracted_windfarm', 'dwt', 'contract_scope', 'amount_turbines', 'manufacturer', 'wec_type', 'actor', 'start_date', 'end_date')
        attrs = {"class": "windfarms"}
        per_page = 25
        empty_text = _("There are no contracts matching the search criteria...")

class TOContractTable(dt2.Table):
    amount_turbines = dt2.Column(verbose_name=_('Amount'), footer=lambda table: sum(x.amount_turbines for x in table.data), orderable=False)
    contracted_windfarm = dt2.Column(accessor='contracted_windfarm_name', verbose_name=_('Wind Farm'), orderable=False)
    manufacturer = dt2.Column(accessor='contracted_oem_name', verbose_name=_('Manufacturer'), orderable=False)
    wec_type = dt2.Column(accessor='contracted_wec_types_name', verbose_name='Model', orderable=False)
    name = dt2.LinkColumn(None, footer='Total')
    start_date = dt2.DateColumn(format='d b Y')
    end_date = dt2.DateColumn(format='d b Y')
    actor = dt2.Column(verbose_name=_('Contractual Partner'))
    contract_scope = dt2.Column(accessor='contract_scope', verbose_name=_('Contract Type'), orderable=False)

    class Meta:
        model = Contract
        fields =('name', 'contracted_windfarm', 'dwt', 'contract_scope', 'amount_turbines', 'manufacturer', 'wec_type', 'actor', 'start_date', 'end_date')
        attrs = {"class": "windfarms"}
        per_page = 25
        empty_text = _("There are no contracts matching the search criteria...")
