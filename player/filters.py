import django_filters
from .models import Player
from wind_farms.models import Country
from dal import autocomplete

class PlayerListFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Name')
    city = django_filters.CharFilter(lookup_expr='icontains', label='City')
    country = django_filters.ModelChoiceFilter(queryset=Country.objects.all(), widget=autocomplete.ModelSelect2(url='turbines:country-autocomplete'))
    #dwt_customer = django_filters.BooleanFilter(name='customer_code', lookup_expr='isnull', exclude=True, label="DWTX customer")

    class Meta:
        model = Player
        fields = ['name', 'country', 'city', 'postal_code', 'web', 'mail', 'adress', 'sector']#, 'dwt_customer']
        order_by = ['pk']