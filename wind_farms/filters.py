from django.db.models import Q

from .models import WindFarm, Country

import django_filters
from dal import autocomplete

class WindFarmListFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method='custom_name_filter')
    country = django_filters.ModelMultipleChoiceFilter(queryset=Country.objects.all(), widget=autocomplete.ModelSelect2Multiple(url='turbines:country-autocomplete'))

    class Meta:
        model = WindFarm
        fields = ['name', 'country', 'offshore']
        order_by = ['pk']

    def custom_name_filter(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(second_name__icontains=value) | Q(city__icontains=value))
