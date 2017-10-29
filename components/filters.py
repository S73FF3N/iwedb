import django_filters
from .models import Component

class ComponentFilter(django_filters.FilterSet):
    weight_t = django_filters.RangeFilter(widget=django_filters.widgets.RangeWidget(attrs={'style': 'width: 48%; display: inline-block;'}))
    manufacturer = django_filters.CharFilter(lookup_expr='icontains', label='Manufacturer')
    name = django_filters.CharFilter(lookup_expr='icontains', label='Name')

    class Meta:
        model = Component
        fields = ['manufacturer', 'name', 'component_type', 'weight_t', 'compatible_to']
        order_by = ['pk']