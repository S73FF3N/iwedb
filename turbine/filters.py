import django_filters
from .models import Turbine

class TurbineListFilter(django_filters.FilterSet):
    commisioning = django_filters.DateFromToRangeFilter(widget=django_filters.widgets.RangeWidget(attrs={'placeholder': 'yyyy/mm/dd', 'style': 'width: 48%; display: inline-block;'}))
    dismantling = django_filters.DateFromToRangeFilter(widget=django_filters.widgets.RangeWidget(attrs={'placeholder': 'yyyy/mm/dd', 'style': 'width: 48%; display: inline-block;'}))
    turbine_id = django_filters.CharFilter(lookup_expr='icontains', label='Turbine ID')
    owner = django_filters.CharFilter(lookup_expr='icontains', label='Owner')
    service = django_filters.CharFilter(lookup_expr='icontains', label='Service Provider')
    developer = django_filters.CharFilter(lookup_expr='icontains', label='Developer')
    com_operator = django_filters.CharFilter(lookup_expr='icontains', label='Commercial Operator')
    tec_operator = django_filters.CharFilter(lookup_expr='icontains', label='Technical Operator')

    class Meta:
        model = Turbine
        fields = ['turbine_id', 'wind_farm', 'wec_manufacturer', 'wec_typ', 'developer', 'owner', 'com_operator', 'tec_operator', 'service', 'offshore', 'status', 'commisioning', 'dismantling']
        order_by = ['pk']