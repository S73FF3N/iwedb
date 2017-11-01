import django_filters
from .models import Component
from polls.models import WEC_Typ
from dal import autocomplete

class ComponentFilter(django_filters.FilterSet):
    weight_t = django_filters.RangeFilter(widget=django_filters.widgets.RangeWidget(attrs={'style': 'width: 48%; display: inline-block;'}))
    manufacturer = django_filters.CharFilter(lookup_expr='icontains', label='Manufacturer')
    name = django_filters.CharFilter(lookup_expr='icontains', label='Name')
    compatible_to = django_filters.ModelChoiceFilter(queryset=WEC_Typ.objects.all(), widget=autocomplete.ModelSelect2Multiple(url='turbines:wec-typ-autocomplete'))

    class Meta:
        model = Component
        fields = ['manufacturer', 'name', 'component_type', 'weight_t', 'compatible_to']
        order_by = ['pk']