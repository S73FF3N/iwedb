from .models import Player
from wind_farms.models import Country

from django.utils.translation import ugettext_lazy as _

import django_filters
from dal import autocomplete

class PlayerListFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Name')
    city = django_filters.CharFilter(lookup_expr='icontains', label=_('City'))
    adress = django_filters.CharFilter(label=_("Address"))
    country = django_filters.ModelChoiceFilter(queryset=Country.objects.all(), widget=autocomplete.ModelSelect2(url='turbines:country-autocomplete'))

    class Meta:
        model = Player
        fields = ['name', 'country', 'city', 'postal_code', 'web', 'mail', 'adress', 'sector']
        order_by = ['pk']