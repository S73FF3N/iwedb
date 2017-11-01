import django_filters
from .models import WindFarm, Country
from dal import autocomplete

class WindFarmListFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Name')
    #amount_turbines = django_filters.RangeFilter(method='filter_amount_turbines')
    #amount_turbines_in_production = django_filters.RangeFilter(action=action)
    country = django_filters.ModelChoiceFilter(queryset=Country.objects.all(), widget=autocomplete.ModelSelect2(url='turbines:country-autocomplete'))

    class Meta:
        model = WindFarm
        fields = ['name', 'country', 'city', 'offshore']#, 'amount_turbines', 'manufacturer', 'wec_typ', 'commisioning', 'status']
        order_by = ['pk']
