import django_filters
from .models import Turbine

class TurbineListFilter(django_filters.FilterSet):
    #commisioning = django_filters.DateFromToRangeFilter()
    turbine_id = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Turbine
        fields = ['turbine_id', 'wind_farm', 'wec_manufacturer', 'wec_typ', 'developer', 'owner', 'com_operator', 'tec_operator', 'service', 'offshore', 'status']
        order_by = ['pk']