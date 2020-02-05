from dal import autocomplete

from django import forms

from .models import Turbine, Contract
from wind_farms.models import WindFarm

class TurbineForm(forms.ModelForm):
    prefix = 'turbine'
    required_css_class = 'required'
    error_css_class = 'required'

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
                    'turbine_id': forms.TextInput(attrs={'placeholder': 'SEN300855', 'id': 'turbine_id_form_field'}),
                    'status': forms.Select(attrs={'id':'status_id'}),
                    }
        labels = {'commisioning_year': 'Commisioning',}

class ContractForm(forms.ModelForm):
    prefix = 'contract'
    required_css_class = 'required'
    error_css_class = 'required'

    windfarm = forms.ModelMultipleChoiceField(queryset=WindFarm.objects.filter(available=True), widget=autocomplete.ModelSelect2Multiple(url='turbines:windfarm-autocomplete'), required=False)
    all_turbines = forms.BooleanField(label="All turbines of selected wind farm?", required=False)
    turbines = forms.ModelMultipleChoiceField(queryset=Turbine.objects.filter(available=True), widget=autocomplete.ModelSelect2Multiple(url='turbines:turbineID-autocomplete', forward=['windfarm']), required=False)

    def clean(self):
        cleaned_data = super(ContractForm, self).clean()
        if cleaned_data['all_turbines'] == True:
            turbines = Turbine.objects.filter(wind_farm__in=cleaned_data['windfarm'], available=True)
            cleaned_data['turbines'] = turbines
        return cleaned_data

    class Meta:
        model = Contract
        form_tag = False
        fields = ('name', 'file', 'dwt', 'dwt_responsible', 'turbines', 'actor', 'start_date', 'end_date', 'average_remuneration',
                    'farm_availability', 'wtg_availability', 'availability_type', 'remote_control', 'scheduled_maintenance',
                    'unscheduled_maintenance_personnel', 'unscheduled_maintenance_material', 'main_components', 'technical_operation', 'external_damages',
                    'service_lift_maintenance', 'additional_maintenance', 'rotor_blade_inspection', 'videoendoscopic_inspection_gearbox', 'safety_inspection',
                    'safety_repairs', 'safety_exchange', 'certified_body_inspection_service_lift', 'pressure_vessels',
                    'periodic_inspection_wtg', 'electrical_inspection', 'exclusions', 'cms', 'overhaul_working_equipment')
        widgets = {'actor': autocomplete.ModelSelect2(url='turbines:actor-autocomplete'),
                   'turbines': autocomplete.ModelSelect2Multiple(url='turbines:turbineID-autocomplete', forward=['windfarm']),
                   'dwt_responsible': autocomplete.ModelSelect2(url='turbines:customer-relations-autocomplete'),
                   'name': forms.TextInput(attrs={'placeholder': 'V-TB-105515-24-02-04_Vollwartungsvertrag_WP XY', 'id': 'contract-name'}),
                   'farm_availability': forms.NumberInput(attrs={'placeholder': '97%',}),
                   'wtg_availability': forms.NumberInput(attrs={'placeholder': '97%',}),
                   'start_date': forms.DateInput(attrs={'type':'date'}),
                   'end_date': forms.DateInput(attrs={'type':'date'}),}
        labels = {'average_remuneration': 'Av. remuneration',
                    'scheduled_maintenance': 'Maintenance',
                    'safety_inspection': 'Safety-related inspection (service lift, safety equipment, etc.)',
                    'safety_repairs': 'Repair service lift, safety equipment, etc.',
                    'safety_exchange': 'Exchange of service lift, safety equipment, etc.',
                    'certified_body_inspection_service_lift': 'Inspection of service lift by certified body',
                    'pressure_vessels': 'Repair of pressure vessels',
                    'periodic_inspection_wtg': 'Periodic Inspection of WTG by independent experts',
                    'cms': 'Condition monitoring',
                    'overhaul_working_equipment': 'General Overhaul of working equipment',}

class TerminationForm(forms.ModelForm):
    prefix = 'termination'

    class Meta:
        model = Contract
        form_tag = False
        fields = ('termination_date', 'termination_reason')
        widgets = {'termination_date': forms.DateInput(attrs={'placeholder': '2019-01-08'}),}

class DuplicateTurbine(forms.Form):
    amount = forms.IntegerField(min_value=1, max_value=999, label="Amount", widget=forms.NumberInput(attrs={'style': "width:35%;"}))
