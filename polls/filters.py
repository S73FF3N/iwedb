import django_filters
from .models import WEC_Typ, Manufacturer
from dal import autocomplete

class WEC_TypFilter(django_filters.FilterSet):
    output_power = django_filters.RangeFilter(widget=django_filters.widgets.RangeWidget(attrs={'style': 'width: 48%; display: inline-block;'}))
    rotor_diameter = django_filters.RangeFilter(widget=django_filters.widgets.RangeWidget(attrs={'style': 'width: 48%; display: inline-block;'}))
    year = django_filters.RangeFilter(widget=django_filters.widgets.RangeWidget(attrs={'placeholder': 'yyyy/mm/dd', 'style': 'width: 48%; display: inline-block;'}))
    manufacturer = django_filters.ModelChoiceFilter(queryset=Manufacturer.objects.all(), widget=autocomplete.ModelSelect2(url='turbines:manufacturer-autocomplete'))

    class Meta:
        model = WEC_Typ
        fields = ['manufacturer', 'name', 'output_power', 'rotor_diameter', 'year', 'offshore', 'reg', 'drive', 'nr_blades']
        order_by = ['pk']