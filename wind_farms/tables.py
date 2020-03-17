import django_tables2 as dt2
from django.utils.translation import ugettext_lazy as _

from .models import WindFarm

class WindFarmTable(dt2.Table):
    name = dt2.LinkColumn(None)
    second_name = dt2.Column(verbose_name="Altenative")
    amount_turbines = dt2.Column(accessor='amount_turbines', verbose_name=_('Turbines'), orderable=False)
    amount_turbines_in_production = dt2.Column(accessor='amount_turbines_in_production', verbose_name=_('in production'), orderable=False)
    first_commisioning = dt2.Column(accessor='get_first_commisioning', verbose_name=_('First Commisioning'), orderable=False)
    offshore_status = dt2.Column(accessor='get_offshore_status', verbose_name='Offshore', orderable=False)
    status = dt2.Column(accessor='get_status', verbose_name='Status', orderable=False)

    class Meta:
        model = WindFarm
        fields =('name', 'second_name', 'country', 'city', 'amount_turbines', 'amount_turbines_in_production', 'first_commisioning', 'offshore_status', 'status')
        attrs = {"class": "windfarms"}
        per_page = 25
        empty_text = _("There are no wind farms matching the search criteria...")