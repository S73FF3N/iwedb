import django_filters
from .models import WindFarm

class WindFarmListFilter(django_filters.FilterSet):
    #amount_turbines = django_filters.RangeFilter()
    #commisioning = django_filters.DateFromToRangeFilter()
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = WindFarm
        fields = ['name', 'country', 'city']#, 'amount_turbines', 'manufacturer', 'wec_typ', 'commisioning', 'developer', 'owner', 'com_operator', 'tec_operator', 'service', 'offshore', 'status']
        order_by = ['pk']
