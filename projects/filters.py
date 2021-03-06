import django_filters

from .models import Project, Calculation_Tool, OfferNumber, PoolProject, CustomerQuestionnaire
from .models import STATUS, CONTRACT_TYPE, DWT, CONTRACT
from player.models import Player
from polls.models import WEC_Typ, Manufacturer
from wind_farms.models import Country, WindFarm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from dal import autocomplete

class ProjectListFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label=_("Project Name"))
    status = django_filters.MultipleChoiceFilter(choices=STATUS)
    customer = django_filters.ModelMultipleChoiceFilter(queryset=Player.objects.all(), widget=autocomplete.ModelSelect2Multiple(url='turbines:actor-autocomplete'))
    prob = django_filters.RangeFilter(widget=django_filters.widgets.RangeWidget(attrs={'placeholder': '50%', 'style': 'width: 48%; display: inline-block;'}))
    start_operation = django_filters.DateFromToRangeFilter(widget=django_filters.widgets.RangeWidget(attrs={'placeholder': 'yyyy-mm-dd', 'style': 'width: 48%; display: inline-block;'}), label=_("Commencement Date"))
    request_date = django_filters.DateFromToRangeFilter(widget=django_filters.widgets.RangeWidget(attrs={'placeholder': 'yyyy-mm-dd', 'style': 'width: 48%; display: inline-block;'}), label=_("Request Date"))
    turbines__wec_typ__manufacturer = django_filters.ModelMultipleChoiceFilter(queryset=Manufacturer.objects.all(), widget=autocomplete.ModelSelect2Multiple(url='turbines:manufacturer-autocomplete'), label=_('Manufacturer'))
    turbines__wec_typ = django_filters.ModelMultipleChoiceFilter(queryset=WEC_Typ.objects.all(), widget=autocomplete.ModelSelect2Multiple(url='turbines:wec-typ-autocomplete', forward=['turbines__wec_typ__manufacturer']), label=_('Model'))
    turbines__wind_farm__country = django_filters.ModelMultipleChoiceFilter(queryset=Country.objects.all(), widget=autocomplete.ModelSelect2Multiple(url='turbines:country-autocomplete'), label=_('Country'))
    contract_signature = django_filters.DateFromToRangeFilter(widget=django_filters.widgets.RangeWidget(attrs={'placeholder': 'yyyy-mm-dd', 'style': 'width: 48%; display: inline-block;'}))
    sales_manager = django_filters.ModelMultipleChoiceFilter(queryset=User.objects.filter(groups__name__in=["Sales"]), widget=autocomplete.ModelSelect2Multiple(url='turbines:user-autocomplete'))
    offer_number = django_filters.ModelChoiceFilter(queryset=OfferNumber.objects.all(), widget=autocomplete.ModelSelect2(url='turbines:offer-number-autocomplete'), label=_("Offer Number"))
    contract = django_filters.MultipleChoiceFilter(choices=CONTRACT)
    contract_type = django_filters.MultipleChoiceFilter(choices=CONTRACT_TYPE, label=_("Scope"))
    dwt = django_filters.MultipleChoiceFilter(choices=DWT, label="DWT")

    class Meta:
        model = Project
        fields = ['name', 'status', 'prob', 'customer', 'dwt', 'start_operation', 'turbines__wec_typ__manufacturer', 'turbines__wec_typ', 'contract', 'contract_type', 'turbines__wind_farm__country', 'contract_signature', 'sales_manager', 'request_date', 'offer_number', 'tender']
        order_by = ['pk']

class PoolProjectFilter(django_filters.FilterSet):
    customer = django_filters.ModelMultipleChoiceFilter(queryset=Player.objects.all(), widget=autocomplete.ModelSelect2Multiple(url='turbines:actor-autocomplete'))
    sales_manager = django_filters.ModelMultipleChoiceFilter(queryset=User.objects.filter(groups__name__in=["Sales"]), widget=autocomplete.ModelSelect2Multiple(url='turbines:user-autocomplete'))
    projects = django_filters.ModelMultipleChoiceFilter(queryset=Project.objects.all(), widget=autocomplete.ModelSelect2Multiple(url='turbines:project-autocomplete'))
    request_date = django_filters.DateFromToRangeFilter(widget=django_filters.widgets.RangeWidget(attrs={'placeholder': 'yyyy-mm-dd', 'style': 'width: 48%; display: inline-block;'}), label=_("Request Date"))

    class Meta:
        model = PoolProject
        fields = ['name', 'sales_manager', 'customer', 'projects', 'request_date']
        order_by = ['pk']

class OfferNumberFilter(django_filters.FilterSet):
    number = django_filters.CharFilter(lookup_expr='icontains', label=_("Offer Number"))
    wec_typ = django_filters.ModelMultipleChoiceFilter(queryset=WEC_Typ.objects.all(), widget=autocomplete.ModelSelect2Multiple(url='turbines:wec-typ-autocomplete', forward=['turbines__wec_typ__manufacturer']), label=_('Model'))
    sales_manager = django_filters.ModelMultipleChoiceFilter(queryset=User.objects.filter(groups__name__in=["Sales"]), widget=autocomplete.ModelSelect2Multiple(url='turbines:user-autocomplete'))
    created_by = django_filters.ModelMultipleChoiceFilter(queryset=User.objects.all(), widget=autocomplete.ModelSelect2Multiple(url='turbines:user-autocomplete'))

    class Meta:
        model = OfferNumber
        fields = ['number', 'wind_farm', 'amount', 'wec_typ', 'sales_manager', 'created_by']
        order_by = ['pk']

class Calculation_ToolFilter(django_filters.FilterSet):
    valid_for_country = django_filters.ModelMultipleChoiceFilter(queryset=Country.objects.all(), widget=autocomplete.ModelSelect2Multiple(url='turbines:country-autocomplete'), label=_('Country'))

    class Meta:
        model = Calculation_Tool
        fields = ['valid_for_country']
        order_by =['-created']

class CustomerQuestionnaireFilter(django_filters.FilterSet):
    wind_farm_name = django_filters.CharFilter(lookup_expr='icontains', label=_("Wind Farm"))

    class Meta:
        model = CustomerQuestionnaire
        fields = ['wind_farm_name']
