import django_filters

from .models import Project
from .models import STATUS
from player.models import Player
from polls.models import WEC_Typ, Manufacturer
from wind_farms.models import Country
from django.contrib.auth.models import User

from dal import autocomplete

class ProjectListFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label="Project Name")
    status = django_filters.MultipleChoiceFilter(choices=STATUS)
    customer = django_filters.ModelChoiceFilter(queryset=Player.objects.all(), widget=autocomplete.ModelSelect2(url='turbines:actor-autocomplete'))
    prob = django_filters.RangeFilter(widget=django_filters.widgets.RangeWidget(attrs={'placeholder': '50%', 'style': 'width: 48%; display: inline-block;'}))
    start_operation = django_filters.DateFromToRangeFilter(widget=django_filters.widgets.RangeWidget(attrs={'placeholder': 'yyyy-mm-dd', 'style': 'width: 48%; display: inline-block;'}), label="Commencement Date")
    request_date = django_filters.DateFromToRangeFilter(widget=django_filters.widgets.RangeWidget(attrs={'placeholder': 'yyyy-mm-dd', 'style': 'width: 48%; display: inline-block;'}), label="Request Date")
    turbines__wec_typ__manufacturer = django_filters.ModelMultipleChoiceFilter(queryset=Manufacturer.objects.all(), widget=autocomplete.ModelSelect2Multiple(url='turbines:manufacturer-autocomplete'), label='Manufacturer')
    turbines__wec_typ = django_filters.ModelMultipleChoiceFilter(queryset=WEC_Typ.objects.all(), widget=autocomplete.ModelSelect2Multiple(url='turbines:wec-typ-autocomplete', forward=['turbines__wec_typ__manufacturer']), label='Model')
    turbines__wind_farm__country = django_filters.ModelMultipleChoiceFilter(queryset=Country.objects.all(), widget=autocomplete.ModelSelect2Multiple(url='turbines:country-autocomplete'), label='Country')
    contract_signature = django_filters.DateFromToRangeFilter(widget=django_filters.widgets.RangeWidget(attrs={'placeholder': 'yyyy-mm-dd', 'style': 'width: 48%; display: inline-block;'}))
    sales_manager = django_filters.ModelMultipleChoiceFilter(queryset=User.objects.filter(groups__name__in=["Sales"]), widget=autocomplete.ModelSelect2Multiple(url='turbines:user-autocomplete'))

    class Meta:
        model = Project
        fields = ['name', 'status', 'prob', 'customer', 'dwt', 'start_operation', 'turbines__wec_typ__manufacturer', 'turbines__wec_typ', 'contract_type', 'turbines__wind_farm__country', 'contract_signature', 'sales_manager', 'request_date'] #'turbines',
        order_by = ['pk']
