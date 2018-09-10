from django import forms
from .models import Turbine, Contract
from django.forms.extras import SelectDateWidget
from dal import autocomplete

YEARS = ('1999', '2000', '2001', '2002', '2003',
       '2004', '2005', '2006', '2007', '2008',
       '2009', '2010', '2011', '2012', '2013',
       '2014', '2015', '2016', '2017', '2018',
       '2019', '2020', '2021', '2022', '2023',
       '2024', '2025', '2026', '2027', '2028',
       '2029', '2030', '2031')

class TurbineForm(forms.ModelForm):
    prefix = 'turbine'
    commisioning = forms.DateField(widget=SelectDateWidget(years=range(1900, 2030), attrs=({'style': 'width: 32%;'})), required=False)
    dismantling = forms.DateField(widget=SelectDateWidget(years=range(1900, 2030), attrs=({'style': 'width: 32%;'})), required=False)

    class Meta:
        model = Turbine
        form_tag = False
        fields = ('turbine_id', 'wind_farm', 'wec_typ', 'commisioning', 'developer', 'asset_management', 'owner', 'com_operator', 'tec_operator', 'service', 'offshore', 'dismantling', 'hub_height', 'longitude', 'latitude', 'repowered', 'follow_up_wec', 'status', 'osm_id')#'wec_manufacturer',
        widgets = {'wind_farm': autocomplete.ModelSelect2(url='turbines:windfarm-autocomplete'),
                    'wec_typ': autocomplete.ModelSelect2(url='turbines:wec-typ-autocomplete'),
                    'developer': autocomplete.ModelSelect2Multiple(url='turbines:actor-autocomplete'),
                    'asset_management': autocomplete.ModelSelect2Multiple(url='turbines:actor-autocomplete'),
                    'com_operator': autocomplete.ModelSelect2Multiple(url='turbines:actor-autocomplete'),
                    'tec_operator': autocomplete.ModelSelect2Multiple(url='turbines:actor-autocomplete'),
                    'service': autocomplete.ModelSelect2Multiple(url='turbines:actor-autocomplete'),
                    'owner': autocomplete.ModelSelect2(url='turbines:actor-autocomplete'),
                    'follow_up_wec': autocomplete.ModelSelect2(url='turbines:turbineID-autocomplete'),
                    'latitude': forms.NumberInput(attrs={'placeholder': '51.45878',}),
                    'longitude': forms.NumberInput(attrs={'placeholder': '6.51999',})
                    }

class ContractForm(forms.ModelForm):
    prefix = 'contract'
    start_date = forms.DateField(widget=SelectDateWidget(years = YEARS, attrs=({'style': 'width: 32%;'})))
    end_date = forms.DateField(widget=SelectDateWidget(years = YEARS, attrs=({'style': 'width: 32%;'})))

    class Meta:
        model = Contract
        form_tag = False
        fields = ('name', 'file', 'turbines', 'actor', 'start_date', 'end_date', 'average_remuneration',
                    'farm_availability', 'wtg_availability', 'remote_control', 'scheduled_maintenance',
                    'unscheduled_maintenance_personnel', 'unscheduled_maintenance_material', 'main_components', 'rotor_excluded', 'external_damages')
        widgets = {'actor': autocomplete.ModelSelect2(url='turbines:actor-autocomplete'),
                   'turbines': autocomplete.ModelSelect2Multiple(url='turbines:turbineID-autocomplete'),
                   'name': forms.TextInput(attrs={'placeholder': 'VB-TB-105515-24-02-04_Vollwartungsvertrag_WP XY'}),
                   'farm_availability': forms.NumberInput(attrs={'placeholder': '97%',}),
                   'wtg_availability': forms.NumberInput(attrs={'placeholder': '97%',}),}
        labels = {'average_remuneration': 'Av. remuneration',
                    'scheduled_maintenance': 'Shed. maintenance',}