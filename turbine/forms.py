from django import forms
from .models import Turbine, Contract
from django.forms.extras import SelectDateWidget

class TurbineForm(forms.ModelForm):
    prefix = 'turbine'
    commisioning = forms.DateField(widget=SelectDateWidget(attrs=({'style': 'width: 32%;'})))
    dismantling = forms.DateField(widget=SelectDateWidget(attrs=({'style': 'width: 32%;'})))
    class Meta:
        model = Turbine
        form_tag = False
        fields = ('turbine_id', 'wind_farm', 'wec_manufacturer', 'wec_typ', 'commisioning', 'developer', 'owner', 'com_operator', 'tec_operator', 'service', 'offshore', 'dismantling', 'hub_height', 'longitude', 'latitude', 'repowered', 'follow_up_wec', 'status')

class ContractForm(forms.ModelForm):
    prefix = 'contract'
    start_date = forms.DateField(widget=SelectDateWidget(attrs=({'style': 'width: 32%;'})))
    end_date = forms.DateField(widget=SelectDateWidget(attrs=({'style': 'width: 32%;'})))
    class Meta:
        model = Contract
        form_tag = False
        fields = ('turbine', 'actor', 'contract_type', 'start_date', 'end_date')