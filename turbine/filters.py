import django_filters
from .models import Turbine
from wind_farms.models import WindFarm
from polls.models import WEC_Typ, Manufacturer
from player.models import Player
from dal import autocomplete

class TurbineListFilter(django_filters.FilterSet):
    commisioning = django_filters.DateFromToRangeFilter(widget=django_filters.widgets.RangeWidget(attrs={'placeholder': 'yyyy/mm/dd', 'style': 'width: 48%; display: inline-block;'}))
    dismantling = django_filters.DateFromToRangeFilter(widget=django_filters.widgets.RangeWidget(attrs={'placeholder': 'yyyy/mm/dd', 'style': 'width: 48%; display: inline-block;'}))
    turbine_id = django_filters.CharFilter(lookup_expr='icontains', label='Turbine ID')
    wind_farm = django_filters.ModelChoiceFilter(queryset=WindFarm.objects.all(), widget=autocomplete.ModelSelect2(url='turbines:windfarm-autocomplete'))
    wec_typ = django_filters.ModelChoiceFilter(queryset=WEC_Typ.objects.all(), widget=autocomplete.ModelSelect2(url='turbines:wec-typ-autocomplete'))
    wec_manufacturer = django_filters.ModelChoiceFilter(queryset=Manufacturer.objects.all(), widget=autocomplete.ModelSelect2(url='turbines:manufacturer-autocomplete'))
    developer = django_filters.ModelChoiceFilter(queryset=Player.objects.all(), widget=autocomplete.ModelSelect2Multiple(url='turbines:actor-autocomplete'))
    com_operator = django_filters.ModelChoiceFilter(queryset=Player.objects.all(), widget=autocomplete.ModelSelect2Multiple(url='turbines:actor-autocomplete'))
    tec_operator = django_filters.ModelChoiceFilter(queryset=Player.objects.all(), widget=autocomplete.ModelSelect2Multiple(url='turbines:actor-autocomplete'))
    service = django_filters.ModelChoiceFilter(queryset=Player.objects.all(), widget=autocomplete.ModelSelect2Multiple(url='turbines:actor-autocomplete'))
    owner = django_filters.ModelChoiceFilter(queryset=Player.objects.all(), widget=autocomplete.ModelSelect2(url='turbines:actor-autocomplete'))

    class Meta:
        model = Turbine
        fields = ['turbine_id', 'wind_farm', 'wec_manufacturer', 'wec_typ', 'developer', 'owner', 'com_operator', 'tec_operator', 'service', 'offshore', 'status', 'commisioning', 'dismantling']
        order_by = ['pk']