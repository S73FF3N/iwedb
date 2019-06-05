import django_filters
from .models import WEC_Typ, Manufacturer
from dal import autocomplete

class WEC_TypFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label="Name")
    output_power = django_filters.RangeFilter(widget=django_filters.widgets.RangeWidget(attrs={'style': 'width: 48%; display: inline-block;'}))
    rotor_diameter = django_filters.RangeFilter(widget=django_filters.widgets.RangeWidget(attrs={'style': 'width: 48%; display: inline-block;'}))
    year = django_filters.RangeFilter(widget=django_filters.widgets.RangeWidget(attrs={'placeholder': 'yyyy-mm-dd', 'style': 'width: 48%; display: inline-block;'}))
    manufacturer = django_filters.ModelMultipleChoiceFilter(queryset=Manufacturer.objects.all(), widget=autocomplete.ModelSelect2Multiple(url='turbines:manufacturer-autocomplete'))

    class Meta:
        model = WEC_Typ
        fields = ['manufacturer', 'name', 'output_power', 'rotor_diameter', 'year', 'offshore', 'reg', 'drive', 'serviced_by_dwt']
        order_by = ['pk']