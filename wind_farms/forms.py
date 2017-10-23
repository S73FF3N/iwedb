from django import forms
from .models import WindFarm

class WindFarmForm(forms.ModelForm):
    prefix = 'wind_farm'
    class Meta:
        model = WindFarm
        form_tag = False
        fields = ('name', 'offshore', 'country', 'city', 'description', 'longitude', 'latitude')
