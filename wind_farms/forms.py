from django import forms
from .models import WindFarm

from dal import autocomplete


class WindFarmForm(forms.ModelForm):
    prefix = 'wind_farm'
    class Meta:
        model = WindFarm
        form_tag = False
        fields = ('name', 'offshore', 'country', 'city', 'description', 'longitude', 'latitude')
        widgets = {'country': autocomplete.ModelSelect2(url='turbines:country-autocomplete')}
