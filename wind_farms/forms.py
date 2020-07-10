from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import WindFarm
from turbine.models import Turbine
from polls.models import WEC_Typ
from projects.forms import HTML5RequiredMixin

from dal import autocomplete

class WindFarmForm(HTML5RequiredMixin, forms.ModelForm):
    prefix = 'wind_farm'

    class Meta:
        model = WindFarm
        form_tag = False
        fields = ('name', 'second_name', 'offshore', 'country', 'postal_code', 'city', 'description', 'longitude', 'latitude')
        labels = {'second_name': _('2nd name'),
                    'country': _('Country'),
                    'postal_code': _('Postal Code'),
                    'city': _('City'),
                    'description': _('Description'),
                    'longitude': _('Longitude'),
                    'latitude': _('Latitude'),}

        widgets = {'name': forms.TextInput(attrs={'id': 'windfarm-name'}),
                    'second_name': forms.TextInput(attrs={'id': 'windfarm-second-name'}),
                    'city': forms.TextInput(attrs={'id': 'windfarm-city-name'}),
                    'country': autocomplete.ModelSelect2(url='turbines:country-autocomplete'),
                    'latitude': forms.NumberInput(attrs={'placeholder': '51.45878',}),
                    'longitude': forms.NumberInput(attrs={'placeholder': '6.51999',}),}

class ChangeTurbineFieldsForm(HTML5RequiredMixin, forms.ModelForm):
    prefix = 'turbine'

    turbines = forms.ModelMultipleChoiceField(queryset=Turbine.objects.filter(available=True), widget=autocomplete.ModelSelect2Multiple(url='turbines:turbineID-autocomplete'))#, forward=['windfarm']
    wind_farm = forms.ModelChoiceField(queryset=WindFarm.objects.filter(available=True), widget=autocomplete.ModelSelect2(url='turbines:windfarm-autocomplete'), required=False)
    wec_typ = forms.ModelChoiceField(queryset=WEC_Typ.objects.filter(available=True), widget=autocomplete.ModelSelect2(url='turbines:wec-typ-autocomplete'), required=False)

    def __init__(self, *args, **kwargs):
        windfarm_pk = kwargs.pop('windfarm_pk')
        super(ChangeTurbineFieldsForm, self).__init__(*args, **kwargs)
        self.fields['turbines'].initial = Turbine.objects.filter(available=True, wind_farm=windfarm_pk)

    class Meta:
        model = Turbine
        form_tag = False
        fields = ('commisioning_year', 'commisioning_month', 'commisioning_day', 'developer', 'asset_management', 'owner', 'com_operator',
                    'tec_operator', 'service', 'offshore', 'dismantling_year', 'dismantling_month', 'dismantling_day', 'hub_height', 'repowered', 'status')
        widgets = {'developer': autocomplete.ModelSelect2Multiple(url='turbines:actor-autocomplete'),
                    'asset_management': autocomplete.ModelSelect2Multiple(url='turbines:actor-autocomplete'),
                    'com_operator': autocomplete.ModelSelect2Multiple(url='turbines:actor-autocomplete'),
                    'tec_operator': autocomplete.ModelSelect2Multiple(url='turbines:actor-autocomplete'),
                    'service': autocomplete.ModelSelect2Multiple(url='turbines:actor-autocomplete'),
                    'owner': autocomplete.ModelSelect2(url='turbines:actor-autocomplete'),
                    'status': forms.Select(attrs={'id':'status_id'}),
                    }
        labels = {'commisioning_year': _('Commisioning'),
                    'commisioning_month': _('Month'),
                    'commisioning_day': _('Day'),
                    'dismantling_month': _('Month'),
                    'dismantling_day': _('Day'),}
        required = {'wec_typ': False,}