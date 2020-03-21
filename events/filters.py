import django_filters
from dal import autocomplete

from .models import Event, EVENTS
from wind_farms.models import WindFarm

from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class EventListFilter(django_filters.FilterSet):
    title = django_filters.MultipleChoiceFilter(choices=EVENTS, label=_("Type"))
    turbines__wind_farm = django_filters.ModelMultipleChoiceFilter(queryset=WindFarm.objects.all(), widget=autocomplete.ModelSelect2Multiple(url='turbines:windfarm-autocomplete'), label=_('Wind Farm'))
    responsibles = django_filters.ModelMultipleChoiceFilter(queryset=User.objects.filter(groups__name__in=["Technical Operations"]), widget=autocomplete.ModelSelect2Multiple(url='turbines:customer-relations-autocomplete'), label=_('Responsible'))

    class Meta:
        model = Event
        fields = ['title', 'turbines__wind_farm', 'responsibles']
        order_by = ['pk']