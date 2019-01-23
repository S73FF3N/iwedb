from dal import autocomplete
import django_filters

from django.db.models import Count

from .models import Turbine, Contract
from wind_farms.models import WindFarm, Country
from polls.models import WEC_Typ, Manufacturer
from player.models import Player

class TurbineListFilter(django_filters.FilterSet):
    commisioning_year = django_filters.RangeFilter(widget=django_filters.widgets.RangeWidget(attrs={'placeholder': '2018', 'style': 'width: 48%; display: inline-block;'}))
    dismantling_year = django_filters.RangeFilter(widget=django_filters.widgets.RangeWidget(attrs={'placeholder': '2018', 'style': 'width: 48%; display: inline-block;'}))
    turbine_id = django_filters.CharFilter(lookup_expr='icontains', label='Turbine ID')
    wind_farm = django_filters.ModelChoiceFilter(queryset=WindFarm.objects.all(), widget=autocomplete.ModelSelect2(url='turbines:windfarm-autocomplete'))
    wec_typ__manufacturer = django_filters.ModelMultipleChoiceFilter(queryset=Manufacturer.objects.all(), widget=autocomplete.ModelSelect2Multiple(url='turbines:manufacturer-autocomplete'), label='Manufacturer')
    wec_typ = django_filters.ModelMultipleChoiceFilter(queryset=WEC_Typ.objects.all(), widget=autocomplete.ModelSelect2Multiple(url='turbines:wec-typ-autocomplete', forward=['wec_typ__manufacturer']), label='Model')
    developer = django_filters.ModelMultipleChoiceFilter(queryset=Player.objects.all(), widget=autocomplete.ModelSelect2Multiple(url='turbines:actor-autocomplete'))
    asset_management = django_filters.ModelMultipleChoiceFilter(queryset=Player.objects.all(), widget=autocomplete.ModelSelect2Multiple(url='turbines:actor-autocomplete'))
    com_operator = django_filters.ModelMultipleChoiceFilter(queryset=Player.objects.all(), widget=autocomplete.ModelSelect2Multiple(url='turbines:actor-autocomplete'))
    tec_operator = django_filters.ModelMultipleChoiceFilter(queryset=Player.objects.all(), widget=autocomplete.ModelSelect2Multiple(url='turbines:actor-autocomplete'))
    service = django_filters.ModelMultipleChoiceFilter(queryset=Player.objects.all(), widget=autocomplete.ModelSelect2Multiple(url='turbines:actor-autocomplete'))
    owner = django_filters.ModelChoiceFilter(queryset=Player.objects.all(), widget=autocomplete.ModelSelect2(url='turbines:actor-autocomplete'))
    wind_farm__country = django_filters.ModelMultipleChoiceFilter(queryset=Country.objects.all(), widget=autocomplete.ModelSelect2Multiple(url='turbines:country-autocomplete'), label='Country')

    class Meta:
        model = Turbine
        fields = ['turbine_id', 'wind_farm', 'wec_typ__manufacturer', 'wec_typ', 'developer', 'asset_management', 'owner', 'com_operator', 'tec_operator', 'service', 'offshore', 'status', 'commisioning_year', 'dismantling_year', 'wind_farm__country']
        order_by = ['pk']

class ContractListFilter(django_filters.FilterSet):
    turbines = django_filters.ModelChoiceFilter(queryset=Turbine.objects.all(), widget=autocomplete.ModelSelect2(url='turbines:turbineID-autocomplete'))
    actor = django_filters.ModelMultipleChoiceFilter(queryset=Player.objects.all(), label="Contractual Partner", widget=autocomplete.ModelSelect2Multiple(url='turbines:actor-autocomplete'))
    start_date = django_filters.DateFromToRangeFilter(widget=django_filters.widgets.RangeWidget(attrs={'placeholder': 'yyyy-mm-dd', 'style': 'width: 48%; display: inline-block;'}))
    end_date = django_filters.DateFromToRangeFilter(widget=django_filters.widgets.RangeWidget(attrs={'placeholder': 'yyyy-mm-dd', 'style': 'width: 48%; display: inline-block;'}))
    turbines__wind_farm = django_filters.ModelChoiceFilter(queryset=WindFarm.objects.all(), widget=autocomplete.ModelSelect2(url='turbines:windfarm-autocomplete'), label="Wind Farm")
    turbines__wec_typ__manufacturer = django_filters.ModelMultipleChoiceFilter(queryset=Manufacturer.objects.all(), widget=autocomplete.ModelSelect2Multiple(url='turbines:manufacturer-autocomplete'), label='Manufacturer')
    turbines__wec_typ = django_filters.ModelMultipleChoiceFilter(queryset=WEC_Typ.objects.all(), widget=autocomplete.ModelSelect2Multiple(url='turbines:wec-typ-autocomplete', forward=['turbines__wec_typ__manufacturer']), label='Model')

    class Meta:
        model = Contract
        fields = ['name', 'turbines', 'actor', 'start_date', 'end_date', 'turbines__wec_typ__manufacturer', 'turbines__wec_typ', 'dwt']
        order_by = ['pk']

    @property
    def amount_wtgs(self):
        qs = super(ContractListFilter, self).qs
        amount_wtgs = qs.annotate(amount_wtgs=Count('turbines'))
        amount_wtgs = [x.amount_turbines for x in qs]
        return sum(amount_wtgs)
