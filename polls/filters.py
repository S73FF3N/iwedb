import django_filters
from .models import WEC_Typ

class WEC_TypListFilter(django_filters.FilterSet):
    output_power = django_filters.RangeFilter(widget=django_filters.widgets.RangeWidget(attrs={'style': 'width: 48%; display: inline-block;'}))
    rotor_diameter = django_filters.RangeFilter(widget=django_filters.widgets.RangeWidget(attrs={'style': 'width: 48%; display: inline-block;'}))
    year = django_filters.RangeFilter(widget=django_filters.widgets.RangeWidget(attrs={'placeholder': 'yyyy/mm/dd', 'style': 'width: 48%; display: inline-block;'}))

    class Meta:
        model = WEC_Typ
        fields = ['manufacturer', 'name', 'output_power', 'rotor_diameter', 'year', 'offshore', 'reg', 'drive', 'nr_blades']
        order_by = ['pk']