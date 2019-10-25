import django_filters
from dal import autocomplete

from .models import Event, EVENTS
from wind_farms.models import WindFarm
from django.contrib.auth.models import User

class EventListFilter(django_filters.FilterSet):
    title = django_filters.MultipleChoiceFilter(choices=EVENTS, label="Typ")
    turbines__wind_farm = django_filters.ModelMultipleChoiceFilter(queryset=WindFarm.objects.all(), widget=autocomplete.ModelSelect2Multiple(url='turbines:windfarm-autocomplete'), label='Windpark')
    responsible = django_filters.ModelMultipleChoiceFilter(queryset=User.objects.filter(groups__name__in=["Technical Operations"]), widget=autocomplete.ModelSelect2Multiple(url='turbines:technical-operations-autocomplete'), label='Verantworlich')

    class Meta:
        model = Event
        fields = ['title', 'turbines__wind_farm', 'responsible']
        order_by = ['pk']