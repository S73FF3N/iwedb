import django_tables2 as dt2
from .models import WindFarm

class WindFarmTable(dt2.Table):
    name = dt2.LinkColumn(None)
    amount_turbines = dt2.Column(accessor='get_turbines_in_farm', verbose_name='Turbines', orderable=False)
    first_commisioning = dt2.Column(accessor='get_first_commisioning', verbose_name='First Commisioning', orderable=False)

    class Meta:
        model = WindFarm
        fields =('name', 'country', 'city', 'amount_turbines', 'first_commisioning')# 'manufacturer', 'wec_typ', 'developer', 'owner', 'com_operator', 'tec_operator', 'service', 'status')
        attrs = {"class": "windfarms"}
        per_page = 20
        empty_text = "There are no wind farms matching the search criteria..."