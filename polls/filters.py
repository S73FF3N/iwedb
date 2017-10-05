import django_filters
from .models import WEC_Typ

class WEC_TypListFilter(django_filters.FilterSet):
    output_power = django_filters.RangeFilter()
    rotor_diameter = django_filters.RangeFilter()
    year = django_filters.RangeFilter()

    class Meta:
        model = WEC_Typ
        fields = ['manufacturer', 'name', 'output_power', 'rotor_diameter', 'year', 'offshore', 'reg', 'drive', 'nr_blades']
        order_by = ['pk']