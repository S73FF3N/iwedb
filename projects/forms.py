from django import forms

from .models import Project, Comment, OfferNumber, Reminder, PoolProject
from turbine.models import Turbine
from wind_farms.models import WindFarm
from polls.models import Manufacturer

from dal import autocomplete

class ProjectForm(forms.ModelForm):
    prefix = 'project'
    required_css_class = 'required'
    error_css_class = 'required'
    windfarm = forms.ModelMultipleChoiceField(queryset=WindFarm.objects.filter(available=True), widget=autocomplete.ModelSelect2Multiple(url='turbines:windfarm-autocomplete'), required=False)
    all_turbines = forms.BooleanField(label="All turbines of selected wind farm?", required=False)
    turbines = forms.ModelMultipleChoiceField(queryset=Turbine.objects.filter(available=True), widget=autocomplete.ModelSelect2Multiple(url='turbines:turbineID-autocomplete', forward=['windfarm']), required=False)

    def clean(self):
        cleaned_data = super(ProjectForm, self).clean()
        if cleaned_data['all_turbines'] == True:
            turbines = Turbine.objects.filter(wind_farm__in=cleaned_data['windfarm'], available=True)
            cleaned_data['turbines'] = turbines
        return cleaned_data

    class Meta:
        model = Project
        form_tag = False
        fields = ('name', 'status', 'prob', 'customer', 'customer_contact', 'contract', 'contract_type', 'run_time', 'request_date', 'start_operation', 'contract_signature', 'price', 'ebt', 'dwt', 'sales_manager', 'offer_number', 'awarding_reason', 'all_turbines', 'windfarm', 'turbines')
        widgets = {'turbines': autocomplete.ModelSelect2Multiple(url='turbines:turbineID-autocomplete', forward=['windfarm']),
                    'customer': autocomplete.ModelSelect2(url='turbines:actor-autocomplete'),
                    'customer_contact': autocomplete.ModelSelect2(url='turbines:person-autocomplete', forward=['customer']),
                    'sales_manager': autocomplete.ModelSelect2(url='turbines:user-autocomplete'),
                    'prob': forms.NumberInput(attrs={'placeholder': 50}),
                    'run_time': forms.NumberInput(attrs={'placeholder': 5}),
                    'start_operation': forms.DateInput(attrs={'placeholder': '2020-01-01'}),
                    'contract_signature': forms.DateInput(attrs={'placeholder': '2019-01-08'}),
                    'price': forms.NumberInput(attrs={'placeholder': 35000}),
                    'ebt': forms.NumberInput(attrs={'placeholder': 15}),
                    'name': forms.TextInput(attrs={'id': 'project-name'}),
                    'offer_number': autocomplete.ModelSelect2(url='turbines:offer-number-autocomplete'),
                    'awarding_reason': forms.Select(attrs={'id':'awarding_reason_form_field'}),
                    'status': forms.Select(attrs={'id':'status_id'}),
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
        fields = ('text', 'date', 'recipient')
        widgets = {'date': forms.DateInput(attrs={'placeholder': '2021-01-08'}),
                    'recipient': autocomplete.ModelSelect2(url='turbines:user-autocomplete'),}

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
