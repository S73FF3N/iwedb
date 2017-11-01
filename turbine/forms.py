from django import forms
from .models import Turbine, Contract
from django.forms.extras import SelectDateWidget
from dal import autocomplete

class TurbineForm(forms.ModelForm):
    prefix = 'turbine'
    commisioning = forms.DateField(widget=SelectDateWidget(years=range(1900, 2030), attrs=({'style': 'width: 32%;'})), required=False)
    dismantling = forms.DateField(widget=SelectDateWidget(years=range(1900, 2030), attrs=({'style': 'width: 32%;'})), required=False)

    class Meta:
        model = Turbine
        form_tag = False
        fields = ('turbine_id', 'wind_farm', 'wec_manufacturer', 'wec_typ', 'commisioning', 'developer', 'owner', 'com_operator', 'tec_operator', 'service', 'offshore', 'dismantling', 'hub_height', 'longitude', 'latitude', 'repowered', 'follow_up_wec', 'status')
        widgets = {'wind_farm': autocomplete.ModelSelect2(url='turbines:windfarm-autocomplete'),
                    'wec_typ': autocomplete.ModelSelect2(url='turbines:wec-typ-autocomplete'),
                    'wec_manufacturer': autocomplete.ModelSelect2(url='turbines:manufacturer-autocomplete'),
                    'developer': autocomplete.ModelSelect2Multiple(url='turbines:actor-autocomplete'),
                    'com_operator': autocomplete.ModelSelect2Multiple(url='turbines:actor-autocomplete'),
                    'tec_operator': autocomplete.ModelSelect2Multiple(url='turbines:actor-autocomplete'),
                    'service': autocomplete.ModelSelect2Multiple(url='turbines:actor-autocomplete'),
                    'owner': autocomplete.ModelSelect2(url='turbines:actor-autocomplete'),
                    'follow_up_wec': autocomplete.ModelSelect2(url='turbines:turbine-autocomplete')}

class ContractForm(forms.ModelForm):
    prefix = 'contract'
    start_date = forms.DateField(widget=SelectDateWidget(attrs=({'style': 'width: 32%;'})))
    end_date = forms.DateField(widget=SelectDateWidget(attrs=({'style': 'width: 32%;'})))
    class Meta:
        model = Contract
        form_tag = False
        fields = ('turbine', 'actor', 'contract_type', 'start_date', 'end_date')