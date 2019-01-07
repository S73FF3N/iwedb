from django.db.models import Q

from .models import WindFarm, Country

import django_filters
from dal import autocomplete

class WindFarmListFilter(django_filters.FilterSet):
    #name = django_filters.CharFilter(lookup_expr='icontains', label='Name')
    name = django_filters.CharFilter(method='custom_name_filter')
    country = django_filters.ModelChoiceFilter(queryset=Country.objects.all(), widget=autocomplete.ModelSelect2(url='turbines:country-autocomplete'))

    class Meta:
        model = WindFarm
        fields = ['name', 'country', 'city', 'offshore']
        order_by = ['pk']

    def custom_name_filter(self, queryset, name, value):
        return queryset.filter((Q(name__contains=value) | Q(second_name__contains=value)))
