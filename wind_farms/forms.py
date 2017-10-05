from django import forms
from .models import WindFarm#, Contract
#from django.forms.extras import SelectDateWidget

class DateInput(forms.DateInput):
    input_type = 'date'

class WindFarmForm(forms.ModelForm):
    prefix = 'wind_farm'
    #commisioning = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    #dismantling = forms.DateField(widget=SelectDateWidget())
    class Meta:
        model = WindFarm
        form_tag = False
        fields = ('name', 'country', 'city', 'description', 'longitude', 'latitude')#, 'amount_turbines', 'manufacturer', 'wec_typ', 'commisioning', 'developer', 'owner', 'com_operator', 'tec_operator', 'service', 'offshore', 'dismantling', 'hub_height', 'repowered', 'follow_up_farm', 'status')
        #widgets= {'commisioning': DateInput(),}

#class ContractForm(forms.ModelForm):
#    prefix = 'contract'
#    class Meta:
#        model = Contract
#        form_tag = False
#        fields = ('windfarm', 'actor', 'contract_type', 'start_date', 'end_date')