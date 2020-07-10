from dal import autocomplete

from django import forms
from django.forms.formsets import BaseFormSet
from django.utils.translation import ugettext_lazy as _

from .models import Turbine, Contract, Component, ComponentName
from wind_farms.models import WindFarm
from projects.forms import HTML5RequiredMixin

class TurbineForm(HTML5RequiredMixin, forms.ModelForm):
    prefix = 'turbine'

    class Meta:
        model = Turbine
        form_tag = False
        fields = ('turbine_id', 'wind_farm', 'wec_typ', 'commisioning_year', 'commisioning_month', 'commisioning_day', 'developer', 'asset_management', 'owner',
                    'com_operator', 'tec_operator', 'service', 'offshore', 'dismantling_year', 'dismantling_month', 'dismantling_day', 'hub_height', 'longitude',
                    'latitude', 'repowered', 'follow_up_wec', 'status', 'osm_id', 'under_contract_until')

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
                    'under_contract_until': forms.DateInput(attrs={'type':'date'}),
                    }
        labels = {'commisioning_year': _('Commisioning'),
                    'turbine_id': _('Turbine ID'),
                    'wind_farm': _('Windfarm'),
                    'wec_typ': _('WEC Type'),
                    'commisioning_month': _('Commisioning Month'),
                    'commisioning_day': _('Commisioning Day'),
                    'developer': _('Developer'),
                    'asset_management': _('Asset Management'),
                    'owner': _('Owner'),
                    'com_operator': _('Commercial Operator'),
                    'tec_operator': _('Technical Operator'),
                    'service': _('Service'),
                    'dismantling_year': _('Dismantling Year'),
                    'dismantling_month': _('Dismantling Month'),
                    'dismantling_day': _('Dismantling Day'),
                    'hub_height': _('Hub Height'),
                    'longitude': _('Longitude'),
                    'latitude': _('Latitude'),
                    'repowered': _('Repowered'),}

class ComponentForm(HTML5RequiredMixin, forms.ModelForm):
    prefix = 'component'

    component_name_verbose = forms.ModelChoiceField(label=_("Component Name"), queryset=ComponentName.objects.all())
    serial_nr = forms.CharField(required=False)
    installation_date = forms.DateField(label=_("Installation Date"), widget=forms.DateInput(attrs={'type':'date'}), required=False)
    dismantling_date = forms.DateField(label=_("Dismantling Date"), widget=forms.DateInput(attrs={'type':'date'}), required=False)

    class Meta:
        model = Component
        form_tag = False
        fields = ('component_manufacturer', 'component_type')

        widgets = {'component_name_verbose': autocomplete.ModelSelect2(url='turbines:component-name-autocomplete'),
                    'installation_date':forms.DateInput(attrs={'type':'date'}),
                    'dismantling_date':forms.DateInput(attrs={'type':'date'}),}
        labels = {'component_name_verbose': _('Component Name'),
                    'component_manufacturer': _('Component Manufacturer'),
                    'component_type': _('Component Type'),
                    'serial_nr': _('Serial Number'),
                    'installation_date': _('Installation Date'),
                    'dismantling_date': _('Dismantling Date'),}

class BaseComponentFormSet(BaseFormSet):
    def clean(self):
        """
        Adds validation to check that no two components have the same component_name or component_type
        and that all components have both an component_name and component_type.
        """
        if any(self.errors):
            return

        for form in self.forms:
            if form.cleaned_data:
                component_name = form.cleaned_data['component_name_verbose']
                component_type = form.cleaned_data['component_type']

                # Check that all components have both an component_name and component_type
                if component_type and not component_name:
                    raise forms.ValidationError(
                        'All components must have an component name.',
                        code='missing_component_name'
                    )
                elif component_name and not component_type:
                    raise forms.ValidationError(
                        'All components must have a component type.',
                        code='missing_component_type'
                    )

class ContractForm(HTML5RequiredMixin, forms.ModelForm):
    prefix = 'contract'

    windfarm = forms.ModelMultipleChoiceField(label=_("Windfarm"), queryset=WindFarm.objects.filter(available=True), widget=autocomplete.ModelSelect2Multiple(url='turbines:windfarm-autocomplete'), required=False)
    all_turbines = forms.BooleanField(label=_("All turbines of selected wind farm?"), required=False)
    turbines = forms.ModelMultipleChoiceField(label=_("Turbines"), queryset=Turbine.objects.filter(available=True), widget=autocomplete.ModelSelect2Multiple(url='turbines:turbineID-autocomplete', forward=['windfarm']), required=False)
    graduated_price_start_year = forms.IntegerField(label=_("Contract Year"), required=False, min_value=0 )
    graduated_price_end_year = forms.IntegerField(label=_("to"), required=False, min_value=0 )
    graduated_price_yearly_price = forms.IntegerField(label=_("Yearly Price"), required=False, min_value=0 )
    graduated_price_id = forms.IntegerField(label=_("ID"), required=False )
    graduated_price_delete = forms.BooleanField(label=_("Delete graduated price"), required=False)

    def clean(self):
        cleaned_data = super(ContractForm, self).clean()
        if cleaned_data['all_turbines'] == True:
            turbines = Turbine.objects.filter(wind_farm__in=cleaned_data['windfarm'], available=True)
            cleaned_data['turbines'] = turbines
        return cleaned_data

    class Meta:
        model = Contract
        form_tag = False
        fields = ('name', 'file', 'dwt', 'dwt_responsible', 'turbines', 'actor', 'start_date', 'end_date', 'graduated_price_start_year', 'graduated_price_end_year', 'graduated_price_yearly_price',
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
        labels = {'graduated_price_start_year': _('Start Year'),
                    'graduated_price_end_year': _('End Year'),
                    'graduated_price_yearly_price': _('Yearly Price'),
                    'scheduled_maintenance': _('Maintenance'),
                    'safety_inspection': _('Safety-related inspection (service lift, safety equipment, etc.)'),
                    'safety_repairs': _('Repair service lift, safety equipment, etc.'),
                    'safety_exchange': _('Exchange of service lift, safety equipment, etc.'),
                    'certified_body_inspection_service_lift': _('Inspection of service lift by certified body'),
                    'pressure_vessels': _('Repair of pressure vessels'),
                    'periodic_inspection_wtg': _('Periodic Inspection of WTG by independent experts'),
                    'cms': _('Condition monitoring'),
                    'overhaul_working_equipment': _('General Overhaul of working equipment'),
                    'file': _('File'),
                    'dwt_responsible': _('DWT responsible'),
                    'actor': _('Actor'),
                    'start_date': _('Start Date'),
                    'end_date': _('End Date'),
                    'farm_availability': _('Farm availability'),
                    'wtg_availability': _('WTG availability'),
                    'availability_type': _('Availability Type'),
                    'remote_control': _('Remote Control'),
                    'unscheduled_maintenance_personnel': _('Unscheduled Maintenance Personnel'),
                    'unscheduled_maintenance_material': _('Unscheduled Maintenance Material'),
                    'main_components': _('Main Components'),
                    'technical_operation': _('Technical Operation'),
                    'external_damages': _('External Damages'),
                    'service_lift_maintenance': _('Service Lift Maintenance'),
                    'additional_maintenance': _('Additional Maintenance'),
                    'rotor_blade_inspection': _('Rotor Blade Inspection'),
                    'videoendoscopic_inspection_gearbox': _('Videoendoscopic Inspection Gearbox'),}

class TerminationForm(HTML5RequiredMixin, forms.ModelForm):
    prefix = 'termination'

    class Meta:
        model = Contract
        form_tag = False
        fields = ('termination_date', 'termination_reason')
        widgets = {'termination_date': forms.DateInput(attrs={'placeholder': '2019-01-08'}),}
        lables = {'termination_date': _('Termination Date'),
                    'termination_reason': _('Termination Reason'),}

class DuplicateTurbine(HTML5RequiredMixin, forms.Form):
    amount = forms.IntegerField(min_value=1, max_value=999, label="Amount", widget=forms.NumberInput(attrs={'style': "width:35%;"}))
