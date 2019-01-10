from dal import autocomplete

from django import forms
from django.forms.extras import SelectDateWidget

from .models import Turbine, Contract
from wind_farms.models import WindFarm

class TurbineForm(forms.ModelForm):
    prefix = 'turbine'
    required_css_class = 'required'
    error_css_class = 'required'
    #commisioning = forms.DateField(widget=SelectDateWidget(years=range(1990, 2030), attrs=({'style': 'width: 32%;'})), required=False)
    #dismantling = forms.DateField(widget=SelectDateWidget(years=range(1990, 2050), attrs=({'style': 'width: 32%;'})), required=False)

    class Meta:
        model = Turbine
        form_tag = False
        fields = ('turbine_id', 'wind_farm', 'wec_typ', 'commisioning_year', 'commisioning_month', 'commisioning_day', 'developer', 'asset_management', 'owner', 'com_operator', 'tec_operator', 'service', 'offshore', 'dismantling_year', 'dismantling_month', 'dismantling_day', 'hub_height', 'longitude', 'latitude', 'repowered', 'follow_up_wec', 'status', 'osm_id')#'commisioning','wec_manufacturer',
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
                    'longitude': forms.NumberInput(attrs={'placeholder': '6.51999',}),
                    'osm_id': forms.TextInput(attrs={'placeholder':'272116284'}),
                    'turbine_id': forms.TextInput(attrs={'placeholder': 'SEN300855'}),
                    }
        labels = {'commisioning_year': 'Commisioning',}

class ContractForm(forms.ModelForm):
    prefix = 'contract'
    required_css_class = 'required'
    error_css_class = 'required'
    start_date = forms.DateField(widget=SelectDateWidget(years = range(1990, 2050), attrs=({'style': 'width: 32%;'})))
    end_date = forms.DateField(widget=SelectDateWidget(years = range(1990, 2050), attrs=({'style': 'width: 32%;'})))
    windfarm = forms.ModelMultipleChoiceField(queryset=WindFarm.objects.filter(available=True), widget=autocomplete.ModelSelect2Multiple(url='turbines:windfarm-autocomplete'), required=False)

    class Meta:
        model = Contract
        form_tag = False
        fields = ('name', 'file', 'dwt', 'turbines', 'actor', 'start_date', 'end_date', 'average_remuneration',
                    'farm_availability', 'wtg_availability', 'remote_control', 'scheduled_maintenance',
                    'unscheduled_maintenance_personnel', 'unscheduled_maintenance_material', 'main_components', 'rotor_excluded', 'external_damages',
                    'service_lift_maintenance', 'additional_maintenance', 'rotor_blade_inspection', 'videoendoscopic_inspection_gearbox', 'safety_inspection',
                    'safety_repairs', 'certified_body_inspection_service_lift', 'pressure_vessels',
                    'periodic_inspection_wtg', 'electrical_inspection')
        widgets = {'actor': autocomplete.ModelSelect2(url='turbines:actor-autocomplete'),
                   'turbines': autocomplete.ModelSelect2Multiple(url='turbines:turbineID-autocomplete', forward=['windfarm']),
                   'name': forms.TextInput(attrs={'placeholder': 'VB-TB-105515-24-02-04_Vollwartungsvertrag_WP XY'}),
                   'farm_availability': forms.NumberInput(attrs={'placeholder': '97%',}),
                   'wtg_availability': forms.NumberInput(attrs={'placeholder': '97%',}),}
        labels = {'average_remuneration': 'Av. remuneration',
                    'scheduled_maintenance': 'Maintenance',
                    'safety_inspection': 'Inspection of Safety Devices',
                    'safety_repairs': 'Repair of Safety Devices',
                    'certified_body_inspection_service_lift': 'Inspection of service lift by certified body',
                    'pressure_vessels': 'Repair of pressure vessels',
                    'periodic_inspection_wtg': 'Periodic Inspection of WTG by independent experts',}

class DuplicateTurbine(forms.Form):
    amount = forms.IntegerField(min_value=1, max_value=99, label="Amount")