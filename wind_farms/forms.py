from django import forms
from .models import WindFarm#, Contract
#from django.forms.extras import SelectDateWidget

class DateInput(forms.DateInput):
    input_type = 'date'

class WindFarmForm(forms.ModelForm):
    prefix = 'wind_farm'
    class Meta:
        model = WindFarm
        form_tag = False
        fields = ('name', 'offshore', 'country', 'city', 'description', 'longitude', 'latitude')#, 'amount_turbines', 'manufacturer', 'wec_typ', 'commisioning', 'developer', 'owner', 'com_operator', 'tec_operator', 'service', 'offshore', 'dismantling', 'hub_height', 'repowered', 'follow_up_farm', 'status')
