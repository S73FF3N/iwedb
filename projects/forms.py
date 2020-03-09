from django import forms
from django.forms import modelformset_factory
import logging

from .models import Project, Comment, OfferNumber, Reminder, PoolProject, CustomerQuestionnaire, Turbine_CustomerQuestionnaire
from turbine.models import Turbine
from wind_farms.models import WindFarm
from polls.models import Manufacturer, WEC_Typ

from dal import autocomplete

class ProjectForm(forms.ModelForm):
    prefix = 'project'
    required_css_class = 'required'
    error_css_class = 'required'

    windfarm = forms.ModelMultipleChoiceField(queryset=WindFarm.objects.filter(available=True), widget=autocomplete.ModelSelect2Multiple(url='turbines:windfarm-autocomplete'), required=False)
    all_turbines = forms.BooleanField(label="All turbines of selected wind farm?", required=False)
    turbines = forms.ModelMultipleChoiceField(queryset=Turbine.objects.filter(available=True), widget=autocomplete.ModelSelect2Multiple(url='turbines:turbineID-autocomplete', forward=['windfarm']), required=False)
    expert_report = forms.BooleanField(label="Is an expert report before the operational commencement necessary?", required=False)
    zop = forms.BooleanField(label="ZOP (machine & tower)", required=False)
    rotor = forms.BooleanField(label="ZOP (rotor)", required=False)
    gearbox_endoscopy = forms.BooleanField(label="Gearbox endoscopic inspection", required=False)

    def clean(self):
        cleaned_data = super(ProjectForm, self).clean()
        if cleaned_data['all_turbines'] == True:
            turbines = Turbine.objects.filter(wind_farm__in=cleaned_data['windfarm'], available=True)
            cleaned_data['turbines'] = turbines
        return cleaned_data

    class Meta:
        model = Project
        form_tag = False
        fields = ('name', 'status', 'prob', 'tender', 'customer', 'customer_contact', 'contract', 'contract_type', 'run_time', 'request_date', 'start_operation', 'contract_signature', 'price', 'ebt', 'dwt', 'sales_manager', 'offer_number', 'awarding_reason', 'all_turbines', 'windfarm', 'turbines', 'parkinfo', 'kundendaten', 'expert_report', 'zop', 'rotor', 'gearbox_endoscopy')
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

class CustomerQuestionnaireForm(forms.ModelForm):
    prefix = 'customerquestionnaire'
    required_css_class = 'required'
    error_css_class = 'required'

    class Meta:
        model = CustomerQuestionnaire
        form_tag = False
        fields = ('scope', 'wind_farm_name', 'street_nr', 'postal_code', 'city', 'location_details', 'amount_wec')

class CustomerQuestionnaireForm2(forms.ModelForm):
    prefix = 'customerquestionnaire'
    required_css_class = 'required'
    error_css_class = 'required'

    class Meta:
        model = CustomerQuestionnaire
        form_tag = False
        fields = ('contractual_partner', 'cp_street_nr', 'cp_postal_code', 'cp_city', 'cp_contact_person', 'cp_phone', 'cp_mail', 'cp_legal_form')

class CustomerQuestionnaireForm3(forms.ModelForm):
    prefix = 'customerquestionnaire'
    required_css_class = 'required'
    error_css_class = 'required'

    class Meta:
        model = CustomerQuestionnaire
        form_tag = False
        fields = ('invoice_recipient', 'ir_street_nr', 'ir_postal_code', 'ir_city', 'ir_contact_person', 'ir_phone', 'ir_mail', 'ir_tax_id', 'ir_invoice_mail')

class CustomerQuestionnaireForm4(forms.ModelForm):
    prefix = 'customerquestionnaire'
    required_css_class = 'required'
    error_css_class = 'required'

    class Meta:
        model = CustomerQuestionnaire
        form_tag = False
        fields = ('bank_institute', 'iban', 'bic', 'vat_nr')

class CustomerQuestionnaireForm5(forms.ModelForm):
    prefix = 'customerquestionnaire'
    required_css_class = 'required'
    error_css_class = 'required'

    class Meta:
        model = CustomerQuestionnaire
        form_tag = False
        fields = ('sa_company', 'sa_street_nr', 'sa_postal_code', 'sa_city', 'sa_information')

class CustomerQuestionnaireForm6(forms.ModelForm):
    prefix = 'customerquestionnaire'
    required_css_class = 'required'
    error_css_class = 'required'

    class Meta:
        model = CustomerQuestionnaire
        form_tag = False
        fields = ('contact_company', 'contact_name', 'contact_position', 'contact_mail')

class Turbine_CustomerQuestionnaireForm(forms.ModelForm):
    prefix = 'turbine_customerquestionnaire'
    required_css_class = 'required'
    error_css_class = 'required'

    manufacturer = forms.ModelChoiceField(queryset=Manufacturer.objects.all(), widget=autocomplete.ModelSelect2(url='turbines:manufacturer-autocomplete'))
    turbine_model = forms.ModelChoiceField(queryset=WEC_Typ.objects.all(), widget=autocomplete.ModelSelect2(url='turbines:wec-typ-autocomplete', forward=['manufacturer']))

    class Meta:
        model = Turbine_CustomerQuestionnaire
        form_tag = False
        fields = ('turbine_id', 'manufacturer', 'turbine_model', 'hub_height', 'comissioning', 'control_system')
        widgets = {'turbine_model': autocomplete.ModelSelect2(url='turbines:wec-typ-autocomplete', forward=['manufacturer']),
                    'manufacturer': autocomplete.ModelSelect2(url='turbines:manufacturer-autocomplete'),
                    'comissioning': forms.DateInput(attrs={'type':'date'})}

from django.forms import BaseModelFormSet

class BaseTurbine_CustomerQuestionnaireFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        log = logging.getLogger(__name__)
        super().__init__(*args, **kwargs)
        questionnaire_pk = kwargs.pop('questionnaire_pk', None)
        log.info('questionnaire_pk: '+str(questionnaire_pk))
        if questionnaire_pk:
            self.queryset = Turbine_CustomerQuestionnaire.objects.filter(customer_questionnaire=CustomerQuestionnaire.objects.get(pk=questionnaire_pk))
        else:
            self.queryset = Turbine_CustomerQuestionnaire.objects.none()

TurbineID_FormSet=modelformset_factory(Turbine_CustomerQuestionnaire, fields=('turbine_id',), formset=BaseTurbine_CustomerQuestionnaireFormSet)
Manufacturer_FormSet=modelformset_factory(Turbine_CustomerQuestionnaire, fields=('manufacturer',), formset=BaseTurbine_CustomerQuestionnaireFormSet)
Turbine_Model_FormSet=modelformset_factory(Turbine_CustomerQuestionnaire, fields=('turbine_model',), formset=BaseTurbine_CustomerQuestionnaireFormSet)
HubHeight_FormSet=modelformset_factory(Turbine_CustomerQuestionnaire, fields=('hub_height',), formset=BaseTurbine_CustomerQuestionnaireFormSet)

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
    distance = forms.FloatField(label="Distance [km]", widget=forms.NumberInput(attrs={'id': 'driving-distance'}))
    hours = forms.FloatField(label="Duration [min]", widget=forms.NumberInput(attrs={'id': 'driving-minutes'}))

class ContractsInCloseDistanceForm(forms.Form):
    distance = forms.FloatField(label="Distance [km]", widget=forms.NumberInput(attrs={'id': 'distance-number'}))

class TurbinesInCloseDistanceForm(forms.Form):
    distance = forms.FloatField(widget=forms.NumberInput(attrs={'id': 'turbines-distance-number'}))
    manufacturer = forms.ModelChoiceField(queryset=Manufacturer.objects.all(), widget=forms.Select(attrs={'id': 'manufacturer-id-field'}))#, widget=autocomplete.ModelSelect2(url='turbines:manufacturer-autocomplete'))
