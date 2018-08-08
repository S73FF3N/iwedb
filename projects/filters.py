import django_filters
from .models import Project
from .models import STATUS
from player.models import Player
from turbine.models import Turbine
from polls.models import WEC_Typ, Manufacturer
from dal import autocomplete

class ProjectListFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label="Project Name")
    turbines = django_filters.ModelChoiceFilter(queryset=Turbine.objects.all(), widget=autocomplete.ModelSelect2(url='turbines:turbineID-autocomplete'))
    status = django_filters.MultipleChoiceFilter(choices=STATUS)
    customer = django_filters.ModelChoiceFilter(queryset=Player.objects.all(), widget=autocomplete.ModelSelect2(url='turbines:actor-autocomplete'))
    last_contact = django_filters.DateFromToRangeFilter(widget=django_filters.widgets.RangeWidget(attrs={'placeholder': 'yyyy-mm-dd', 'style': 'width: 48%; display: inline-block;'}))
    prob = django_filters.RangeFilter(widget=django_filters.widgets.RangeWidget(attrs={'placeholder': '50%', 'style': 'width: 48%; display: inline-block;'}))
    responsible = django_filters.CharFilter(lookup_expr='icontains', label="Responsible")
    start_operation = django_filters.DateFromToRangeFilter(widget=django_filters.widgets.RangeWidget(attrs={'placeholder': 'yyyy-mm-dd', 'style': 'width: 48%; display: inline-block;'}), label="Commencement Date")
    turbines__wec_typ__manufacturer = django_filters.ModelMultipleChoiceFilter(queryset=Manufacturer.objects.all(), widget=autocomplete.ModelSelect2Multiple(url='turbines:manufacturer-autocomplete'), label='Manufacturer')
    turbines__wec_typ = django_filters.ModelMultipleChoiceFilter(queryset=WEC_Typ.objects.all(), widget=autocomplete.ModelSelect2Multiple(url='turbines:wec-typ-autocomplete', forward=['turbines__wec_typ__manufacturer']), label='Model')

    class Meta:
        model = Project
        fields = ['name', 'turbines', 'status', 'prob', 'customer', 'last_contact', 'responsible', 'dwt', 'start_operation', 'turbines__wec_typ__manufacturer', 'turbines__wec_typ']
        order_by = ['pk']
