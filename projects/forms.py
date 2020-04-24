from django import forms
from django.forms import modelformset_factory
from modeltranslation.forms import TranslationModelForm
from django.contrib.admin.widgets import AdminFileWidget
from django.forms.widgets import HiddenInput, FileInput
from django.utils.translation import ugettext_lazy as _
#import logging

from .models import Project, Comment, OfferNumber, Reminder, PoolProject, CustomerQuestionnaire, Turbine_CustomerQuestionnaire
from turbine.models import Turbine
from wind_farms.models import WindFarm
from polls.models import Manufacturer, WEC_Typ

from dal import autocomplete

class ProjectForm(forms.ModelForm):
    prefix = 'project'
    required_css_class = 'required'
    error_css_class = 'required'

    windfarm = forms.ModelMultipleChoiceField(label=_("Windfarm"), queryset=WindFarm.objects.filter(available=True), widget=autocomplete.ModelSelect2Multiple(url='turbines:windfarm-autocomplete'), required=False)
    all_turbines = forms.BooleanField(label=_("All turbines of selected wind farm?"), required=False)
    turbines = forms.ModelMultipleChoiceField(label=_("Turbine"), queryset=Turbine.objects.filter(available=True), widget=autocomplete.ModelSelect2Multiple(url='turbines:turbineID-autocomplete', forward=['windfarm']), required=False)
    expert_report = forms.BooleanField(label=_("Is an expert report before the operational commencement necessary?"), required=False)
    zop = forms.BooleanField(label=_("ZOP (machine & tower)"), required=False)
    rotor = forms.BooleanField(label=_("ZOP (rotor)"), required=False)
    gearbox_endoscopy = forms.BooleanField(label=_("Gearbox endoscopic inspection"), required=False)

    def clean(self):
        cleaned_data = super(ProjectForm, self).clean()
        if cleaned_data['all_turbines'] == True:
            turbines = Turbine.objects.filter(wind_farm__in=cleaned_data['windfarm'], available=True)
            cleaned_data['turbines'] = turbines
        return cleaned_data

    class Meta:
        model = Project
        form_tag = False
        fields = ('name', 'status', 'prob', 'tender', 'customer', 'customer_contact', 'contract', 'contract_type', 'run_time', 'request_date', 'start_operation', 'contract_signature', 'price', 'ebt', 'dwt', 'sales_manager',
                    'offer_number', 'awarding_reason', 'all_turbines', 'windfarm', 'turbines', 'parkinfo', 'kundendaten', 'expert_report', 'zop', 'rotor', 'gearbox_endoscopy')
        widgets = {'turbines': autocomplete.ModelSelect2Multiple(url='turbines:turbineID-autocomplete', forward=['windfarm']),
                    'customer': autocomplete.ModelSelect2(url='turbines:actor-autocomplete'),
                    'customer_contact': autocomplete.ModelSelect2(url='turbines:person-autocomplete', forward=['customer']),
                    'sales_manager': autocomplete.ModelSelect2(url='turbines:user-autocomplete'),
                    'prob': forms.NumberInput(attrs={'placeholder': 50}),
                    'run_time': forms.NumberInput(attrs={'placeholder': 5}),
                    'price': forms.NumberInput(attrs={'placeholder': 35000}),
                    'ebt': forms.NumberInput(attrs={'placeholder': 15}),
                    'name': forms.TextInput(attrs={'id': 'project-name'}),
                    'offer_number': autocomplete.ModelSelect2(url='turbines:offer-number-autocomplete'),
                    'awarding_reason': forms.Select(attrs={'id':'awarding_reason_form_field'}),
                    'status': forms.Select(attrs={'id':'status_id'}),
                    'request_date': forms.DateInput(attrs={'type':'date'}),
                    'start_operation': forms.DateInput(attrs={'type':'date'}),
                    'contract_signature': forms.DateInput(attrs={'type':'date'}),
                    }
        labels = {'tender': _('Tender'),
                    'customer': _('Customer'),
                    'customer_contact': _('Customer Contact'),
                    'contract': _('Contract'),
                    'contract_type': _('Contract Type'),
                    'run_time': _('Run Time'),
                    'request_date': _('Request Date'),
                    'start_operation': _('Start Operation'),
                    'contract_signature': _('Contract Signature'),
                    'price': _('Price'),
                    'sales_manager': _('Sales Manager'),
                    'offer_number': _('Offer Number'),
                    'awarding_reason': _('Awarding Reason'),
                    'all_turbines': _('All Turbines'),
                    'windfarm': _('Windfarm'),
                    'turbines': _('Turbines'),
                    'parkinfo': _('Windfarm Information'),
                    'expert_report': _('Expert Report'),
                    'rotor': _('Rotor'),
                    'gearbox_endoscopy': _('Gearbox Endoscopy'),}


class PoolProjectForm(forms.ModelForm):
    prefix = 'poolproject'
    required_css_class = 'required'
    error_css_class = 'required'

    class Meta:
        model = PoolProject
        form_tag = False
        fields = ('name', 'projects', 'customer', 'customer_contact', 'sales_manager', 'request_date')
        widgets = {'projects': autocomplete.ModelSelect2Multiple(url='turbines:project-autocomplete'),
                    'customer': autocomplete.ModelSelect2(url='turbines:actor-autocomplete'),
                    'customer_contact': autocomplete.ModelSelect2(url='turbines:person-autocomplete', forward=['customer']),
                    'sales_manager': autocomplete.ModelSelect2(url='turbines:user-autocomplete'),
                    }
        labels = {'projects': _('Projects'),
                    'customer': _('Customer'),
                    'sales_manager': _('Sales Manager'),
                    'customer_contact': _('Customer Contact'),
                    'request_date': _('Request Date'),}

class HTML5RequiredMixin(object):

    def __init__(self, *args, **kwargs):
        super(HTML5RequiredMixin, self).__init__(*args, **kwargs)
        for field in self.fields:
            if (self.fields[field].required and
               type(self.fields[field].widget) not in
                    (AdminFileWidget, HiddenInput, FileInput) and
               '__prefix__' not in self.fields[field].widget.attrs):

                    self.fields[field].widget.attrs['required'] = 'required'

class ContactForm(HTML5RequiredMixin, forms.ModelForm):
    prefix = 'customerquestionnaire'
    required_css_class = 'required'
    error_css_class = 'required'

    class Meta:
        model = CustomerQuestionnaire
        form_tag = False
        fields = ('contact_company', 'contact_name', 'contact_position', 'contact_mail')
        labels = {'contact_company': _('Contact Company'),
                    'contact_name': _('Contact Name'),
                    'contact_position': _('Contact Position'),
                    'contact_mail': _('Contact Mail'),}

class CQBaseForm(HTML5RequiredMixin, TranslationModelForm):
    prefix = 'customerquestionnaire'
    required_css_class = 'required'
    error_css_class = 'required'

    class Meta:
        model = CustomerQuestionnaire
        form_tag = False
        fields = ('scope', 'wind_farm_name', 'street_nr', 'postal_code', 'city', 'location_details', 'amount_wec')
        labels = {'scope': _('Scope'),
                    'wind_farm_name': _('Windfarm Name'),
                    'street_nr': _('Street Number'),
                    'postal_code': _('Postal Code'),
                    'city': _('City'),
                    'location_details': _('Location Details'),
                    'amount_wec': _('Amount WEC'),}

class ContractualPartnerForm(HTML5RequiredMixin, forms.ModelForm):
    prefix = 'customerquestionnaire'
    required_css_class = 'required'
    error_css_class = 'required'

    class Meta:
        model = CustomerQuestionnaire
        form_tag = False
        fields = ('contractual_partner', 'cp_street_nr', 'cp_postal_code', 'cp_city', 'cp_contact_person', 'cp_phone', 'cp_mail', 'cp_legal_form')

class APOnsiteForm(HTML5RequiredMixin, forms.ModelForm):
    prefix = 'customerquestionnaire'
    required_css_class = 'required'
    error_css_class = 'required'

    class Meta:
        model = CustomerQuestionnaire
        form_tag = False
        fields = ('authorized_person_on_site', 'ap_street_nr', 'ap_postal_code', 'ap_city', 'ap_phone', 'ap_mail')#'ap_contact_person',

class IRForm(HTML5RequiredMixin, forms.ModelForm):
    prefix = 'customerquestionnaire'
    required_css_class = 'required'
    error_css_class = 'required'

    class Meta:
        model = CustomerQuestionnaire
        form_tag = False
        fields = ('invoice_recipient', 'ir_street_nr', 'ir_postal_code', 'ir_city', 'ir_contact_person', 'ir_phone', 'ir_mail', 'ir_tax_id', 'ir_invoice_mail')

class BankDataForm(HTML5RequiredMixin, forms.ModelForm):
    prefix = 'customerquestionnaire'
    required_css_class = 'required'
    error_css_class = 'required'

    class Meta:
        model = CustomerQuestionnaire
        form_tag = False
        fields = ('bank_institute', 'iban', 'bic')#, 'vat_nr')

class ShippingAddressForm(HTML5RequiredMixin, forms.ModelForm):
    prefix = 'customerquestionnaire'
    required_css_class = 'required'
    error_css_class = 'required'

    class Meta:
        model = CustomerQuestionnaire
        form_tag = False
        fields = ('sa_company', 'sa_street_nr', 'sa_postal_code', 'sa_city', 'sa_information')

class COForm(HTML5RequiredMixin, forms.ModelForm):
    prefix = 'customerquestionnaire'
    required_css_class = 'required'
    error_css_class = 'required'

    class Meta:
        model = CustomerQuestionnaire
        form_tag = False
        fields = ('commercial_operator', 'co_street_nr', 'co_postal_code', 'co_city', 'co_contact_person', 'co_phone', 'co_mail')

class TOForm(HTML5RequiredMixin, forms.ModelForm):
    prefix = 'customerquestionnaire'
    required_css_class = 'required'
    error_css_class = 'required'

    class Meta:
        model = CustomerQuestionnaire
        form_tag = False
        fields = ('technical_operator', 'to_street_nr', 'to_postal_code', 'to_city', 'to_contact_person', 'to_phone', 'to_mail')

class ContractStatusForm(HTML5RequiredMixin, forms.ModelForm):
    prefix = 'customerquestionnaire'
    required_css_class = 'required'
    error_css_class = 'required'

    class Meta:
        model = CustomerQuestionnaire
        form_tag = False
        fields = ('current_service_contract', 'commencement_current_service_contract', 'desired_service_contract', 'desired_duration_service_contract')
        widgets = {'commencement_current_service_contract': forms.DateInput(attrs={'type':'date'})}

class DocumentationForm(HTML5RequiredMixin, forms.ModelForm):
    prefix = 'customerquestionnaire'
    required_css_class = 'required'
    error_css_class = 'required'

    class Meta:
        model = CustomerQuestionnaire
        form_tag = False
        fields = ('key_safe_location', 'key_safe_code', 'alarm_system', 'alarm_system_information', 'roadmap', 'single_line_diagram')

class CommunicationForm(HTML5RequiredMixin, forms.ModelForm):
    prefix = 'customerquestionnaire'
    required_css_class = 'required'
    error_css_class = 'required'

    class Meta:
        model = CustomerQuestionnaire
        form_tag = False
        fields = ('it_contact_person', 'it_phone', 'it_mail', 'substation', 'direct_marketing', 'direct_marketer', 'metering_point', 'grid_operator')

class Turbine_CustomerQuestionnaireForm(TranslationModelForm):
    prefix = 'turbine_customerquestionnaire'
    required_css_class = 'required'
    error_css_class = 'required'

    def __init__(self, *args, **kwargs):
        self.questionnaire_pk = kwargs.pop('questionnaire_pk')
        super(Turbine_CustomerQuestionnaireForm, self).__init__(*args, **kwargs)

    manufacturer = forms.ModelChoiceField(queryset=Manufacturer.objects.all(), widget=autocomplete.ModelSelect2(url='turbines:manufacturer-autocomplete'))
    turbine_model = forms.ModelChoiceField(queryset=WEC_Typ.objects.all(), widget=autocomplete.ModelSelect2(url='turbines:wec-typ-autocomplete', forward=['manufacturer']))

    class Meta:
        model = Turbine_CustomerQuestionnaire
        form_tag = False
        fields = '__all__'
        widgets = {'turbine_model': autocomplete.ModelSelect2(url='turbines:wec-typ-autocomplete', forward=['manufacturer']),
                    'manufacturer': autocomplete.ModelSelect2(url='turbines:manufacturer-autocomplete'),
                    'comissioning': forms.DateInput(attrs={'type':'date'})}

from django.forms import BaseModelFormSet

class BaseTurbine_CustomerQuestionnaireFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        self.questionnaire_pk = kwargs.pop('questionnaire_pk', None)
        super(BaseTurbine_CustomerQuestionnaireFormSet, self).__init__(*args, **kwargs)
        if self.questionnaire_pk:
            self.queryset = Turbine_CustomerQuestionnaire.objects.filter(customer_questionnaire=CustomerQuestionnaire.objects.get(pk=self.questionnaire_pk))
            self.extra = 0
        else:
            self.queryset = Turbine_CustomerQuestionnaire.objects.none()
        for form in self.forms:
            for field in form.fields:
                if (form.fields[field].required and
                   type(form.fields[field].widget) not in
                        (AdminFileWidget, HiddenInput, FileInput) and
                   '__prefix__' not in form.fields[field].widget.attrs):

                        form.fields[field].widget.attrs['required'] = 'required'

TurbineID_FormSet=modelformset_factory(Turbine_CustomerQuestionnaire, fields=('turbine_id', 'comissioning',), widgets = {'comissioning': forms.DateInput(attrs={'type':'date'})}, formset=BaseTurbine_CustomerQuestionnaireFormSet)
Turbine_Model_FormSet=modelformset_factory(Turbine_CustomerQuestionnaire, fields=('manufacturer','turbine_model',), widgets = {'turbine_model': autocomplete.ModelSelect2(url='turbines:wec-typ-autocomplete', forward=['manufacturer']), 'manufacturer': autocomplete.ModelSelect2(url='turbines:manufacturer-autocomplete')}, formset=BaseTurbine_CustomerQuestionnaireFormSet)
ServiceLift_FormSet=modelformset_factory(Turbine_CustomerQuestionnaire, fields=('service_lift', 'service_lift_type',), formset=BaseTurbine_CustomerQuestionnaireFormSet)
GeoLocation_FormSet=modelformset_factory(Turbine_CustomerQuestionnaire, fields=('latitude', 'longitude',), formset=BaseTurbine_CustomerQuestionnaireFormSet)
Ladder_FormSet=modelformset_factory(Turbine_CustomerQuestionnaire, fields=('ladder','arrester_system',), formset=BaseTurbine_CustomerQuestionnaireFormSet)
ControlSystem_FormSet=modelformset_factory(Turbine_CustomerQuestionnaire, fields=('output_power','control_system',), formset=BaseTurbine_CustomerQuestionnaireFormSet)
TowerType_FormSet=modelformset_factory(Turbine_CustomerQuestionnaire, fields=('tower_type','hub_height',), formset=BaseTurbine_CustomerQuestionnaireFormSet)
CMS_FormSet=modelformset_factory(Turbine_CustomerQuestionnaire, fields=('cms', 'cms_type',), formset=BaseTurbine_CustomerQuestionnaireFormSet)
IceSensor_FormSet=modelformset_factory(Turbine_CustomerQuestionnaire, fields=('ice_sensor', 'ice_sensor_type',), formset=BaseTurbine_CustomerQuestionnaireFormSet)
FlickerDetection_FormSet=modelformset_factory(Turbine_CustomerQuestionnaire, fields=('flicker_detection', 'flicker_detection_type',), formset=BaseTurbine_CustomerQuestionnaireFormSet)
ObstacleLight_FormSet=modelformset_factory(Turbine_CustomerQuestionnaire, fields=('obstacle_light_system', 'obstacle_light_manufacturer', 'obstacle_light_type',), formset=BaseTurbine_CustomerQuestionnaireFormSet)
Antenna_FormSet=modelformset_factory(Turbine_CustomerQuestionnaire, fields=('antenna', 'antenna_type',), formset=BaseTurbine_CustomerQuestionnaireFormSet)
SDL_FormSet=modelformset_factory(Turbine_CustomerQuestionnaire, fields=('sdl', 'feed_in_tarif',), formset=BaseTurbine_CustomerQuestionnaireFormSet)
YearlyProduction_FormSet=modelformset_factory(Turbine_CustomerQuestionnaire, fields=('yearly_production_1', 'yearly_production_2', 'yearly_production_3',), formset=BaseTurbine_CustomerQuestionnaireFormSet)
Maintenance_FormSet=modelformset_factory(Turbine_CustomerQuestionnaire, fields=('recent_maintenance', 'date_of_recent_maintenance', 'date_of_5_year_maintenance', 'date_of_transformer_maintenance', 'date_of_converter_maintenance', 'date_of_lattice_maintenance', 'date_of_overhaul_winch',), widgets = {'date_of_recent_maintenance': forms.DateInput(attrs={'type':'date'}), 'date_of_5_year_maintenance': forms.DateInput(attrs={'type':'date'}), 'date_of_transformer_maintenance': forms.DateInput(attrs={'type':'date'}), 'date_of_converter_maintenance': forms.DateInput(attrs={'type':'date'}), 'date_of_lattice_maintenance': forms.DateInput(attrs={'type':'date'}), 'date_of_overhaul_winch': forms.DateInput(attrs={'type':'date'})}, formset=BaseTurbine_CustomerQuestionnaireFormSet)
OilExchange_FormSet=modelformset_factory(Turbine_CustomerQuestionnaire, fields=('date_oil_exchange_main_bearing', 'oil_type_main_bearing', 'date_oil_exchange_yaw_gearbox', 'oil_type_yaw_gearbox', 'date_oil_exchange_yaw_bearing', 'oil_type_yaw_bearing', 'date_oil_exchange_pitch_gearbox', 'oil_type_pitch_gearbox', 'date_oil_exchange_hydraulic', 'oil_type_hydraulic',), widgets = {'date_oil_exchange_main_bearing': forms.DateInput(attrs={'type':'date'}), 'date_oil_exchange_yaw_gearbox': forms.DateInput(attrs={'type':'date'}), 'date_oil_exchange_yaw_bearing': forms.DateInput(attrs={'type':'date'}), 'date_oil_exchange_pitch_gearbox': forms.DateInput(attrs={'type':'date'}), 'date_oil_exchange_hydraulic': forms.DateInput(attrs={'type':'date'})}, formset=BaseTurbine_CustomerQuestionnaireFormSet)
Inspection_FormSet=modelformset_factory(Turbine_CustomerQuestionnaire, fields=('date_cb_inspection_machine_tower', 'date_recurring_inspection', 'date_rotor_blade_inspection', 'date_gearbox_endoscopy', 'date_safety_inspection', 'date_service_lift_maintenance', 'date_service_lift_inspection', 'date_electric_inspection', 'date_blade_bearing_inspection',), widgets = {'date_cb_inspection_machine_tower': forms.DateInput(attrs={'type':'date'}), 'date_recurring_inspection': forms.DateInput(attrs={'type':'date'}), 'date_rotor_blade_inspection': forms.DateInput(attrs={'type':'date'}), 'date_gearbox_endoscopy': forms.DateInput(attrs={'type':'date'}), 'date_safety_inspection': forms.DateInput(attrs={'type':'date'}), 'date_service_lift_maintenance': forms.DateInput(attrs={'type':'date'}), 'date_service_lift_inspection': forms.DateInput(attrs={'type':'date'}), 'date_electric_inspection': forms.DateInput(attrs={'type':'date'}), 'date_blade_bearing_inspection': forms.DateInput(attrs={'type':'date'}), }, formset=BaseTurbine_CustomerQuestionnaireFormSet)
Reports_FormSet=modelformset_factory(Turbine_CustomerQuestionnaire, fields=('expert_report',), widgets= { 'expert_report': forms.ClearableFileInput(attrs={'multiple': True})}, formset=BaseTurbine_CustomerQuestionnaireFormSet)
Gearbox_FormSet=modelformset_factory(Turbine_CustomerQuestionnaire, fields=('gearbox_manufacturer', 'gearbox_type', 'gearbox_serialnr', 'gearbox_year',), formset=BaseTurbine_CustomerQuestionnaireFormSet)
Generator_FormSet=modelformset_factory(Turbine_CustomerQuestionnaire, fields=('generator_manufacturer', 'generator_type', 'generator_serialnr', 'generator_year',), formset=BaseTurbine_CustomerQuestionnaireFormSet)
RotorBlade_FormSet=modelformset_factory(Turbine_CustomerQuestionnaire, fields=('rotor_blade_manufacturer', 'rotor_blade_type', 'rotor_blade_serialnr', 'rotor_blade_year',), formset=BaseTurbine_CustomerQuestionnaireFormSet)
Converter_FormSet=modelformset_factory(Turbine_CustomerQuestionnaire, fields=('converter_manufacturer', 'converter_type', 'converter_serialnr', 'converter_year',), formset=BaseTurbine_CustomerQuestionnaireFormSet)

class CommentForm(forms.ModelForm):
    prefix = 'comment'
    required_css_class = 'required'
    error_css_class = 'required'

    class Meta:
        model = Comment
        form_tag = False
        fields = ('text', 'file')

class ReminderForm(forms.ModelForm):
    prefix = 'reminder'
    required_css_class = 'required'
    error_css_class = 'required'

    class Meta:
        model = Reminder
        form_tag = False
        fields = ('text', 'date', 'multiple_recipients')
        widgets = {'date': forms.DateInput(attrs={'placeholder': '2021-01-08'}),
                    'multiple_recipients': autocomplete.ModelSelect2Multiple(url='turbines:user-autocomplete'),}

class OfferNumberForm(forms.ModelForm):
    prefix = 'offer_number'
    required_css_class = 'required'
    error_css_class = 'required'

    class Meta:
        model = OfferNumber
        form_tag = False
        fields = ('number','wind_farm', 'amount', 'wec_typ', 'sales_manager', 'text', 'dwt')
        widgets = {'sales_manager': autocomplete.ModelSelect2(url='turbines:user-autocomplete'),
                    'wec_typ': autocomplete.ModelSelect2(url='turbines:wec-typ-autocomplete'),
                    'number': forms.TextInput(attrs={'readonly':'readonly'}),
                    'dwt': forms.Select(attrs={'id': 'offer_number_dwt'}),}


class DrivingForm(forms.Form):
    distance = forms.FloatField(label=_("Distance [km]"), widget=forms.NumberInput(attrs={'id': 'driving-distance'}))
    hours = forms.FloatField(label=_("Duration [min]"), widget=forms.NumberInput(attrs={'id': 'driving-minutes'}))

class ContractsInCloseDistanceForm(forms.Form):
    distance = forms.FloatField(label=_("Distance [km]"), widget=forms.NumberInput(attrs={'id': 'distance-number'}))

class TurbinesInCloseDistanceForm(forms.Form):
    distance = forms.FloatField(widget=forms.NumberInput(attrs={'id': 'turbines-distance-number'}))
    manufacturer = forms.ModelChoiceField(queryset=Manufacturer.objects.all(), widget=forms.Select(attrs={'id': 'manufacturer-id-field'}))#, widget=autocomplete.ModelSelect2(url='turbines:manufacturer-autocomplete'))
