import django_filters
from .models import Component

class ComponentFilter(django_filters.FilterSet):
    weight_t = django_filters.RangeFilter()

    class Meta:
        model = Component
        fields = ['manufacturer', 'name', 'component_type', 'weight_t']
        order_by = ['pk']