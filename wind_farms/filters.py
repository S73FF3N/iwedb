import django_filters
from .models import WindFarm, Country
from dal import autocomplete

class WindFarmListFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Name')
    country = django_filters.ModelChoiceFilter(queryset=Country.objects.all(), widget=autocomplete.ModelSelect2(url='turbines:country-autocomplete'))

    class Meta:
        model = WindFarm
        fields = ['name', 'country', 'city', 'offshore']
        order_by = ['pk']
