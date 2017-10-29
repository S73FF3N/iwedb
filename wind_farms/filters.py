import django_filters
from .models import WindFarm

class WindFarmListFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Name')

    class Meta:
        model = WindFarm
        fields = ['name', 'country', 'city']#, 'amount_turbines', 'manufacturer', 'wec_typ', 'commisioning', 'offshore', 'status']
        order_by = ['pk']
