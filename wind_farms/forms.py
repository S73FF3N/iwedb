from django import forms
from .models import WindFarm

from dal import autocomplete


class WindFarmForm(forms.ModelForm):
    prefix = 'wind_farm'
    required_css_class = 'required'
    error_css_class = 'required'

    class Meta:
        model = WindFarm
        form_tag = False
        fields = ('name', 'second_name', 'offshore', 'country', 'postal_code', 'city', 'description', 'longitude', 'latitude')
        labels = {'second_name': '2nd name'}
        widgets = {'name': forms.TextInput(attrs={'id': 'windfarm-name'}),
                    'second_name': forms.TextInput(attrs={'id': 'windfarm-second-name'}),
                    'city': forms.TextInput(attrs={'id': 'windfarm-city-name'}),
                    'country': autocomplete.ModelSelect2(url='turbines:country-autocomplete'),
                    'latitude': forms.NumberInput(attrs={'placeholder': '51.45878',}),
                    'longitude': forms.NumberInput(attrs={'placeholder': '6.51999',}),}
