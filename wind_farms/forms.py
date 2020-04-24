from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import WindFarm
from turbine.models import Turbine
from polls.models import WEC_Typ

from dal import autocomplete

class WindFarmForm(forms.ModelForm):
    prefix = 'wind_farm'
    required_css_class = 'required'
    error_css_class = 'required'

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

class ChangeTurbineFieldsForm(forms.ModelForm):
    prefix = 'turbine'
    required_css_class = 'required'
    error_css_class = 'required'

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
        labels = {'commisioning_year': _('Commisioning'),}
        required = {'wec_typ': False,}