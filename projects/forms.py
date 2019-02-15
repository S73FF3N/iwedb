from django import forms

from .models import Project, Comment, OfferNumber
from wind_farms.models import WindFarm

from dal import autocomplete
from datetime import datetime

class ProjectForm(forms.ModelForm):
    prefix = 'project'
    required_css_class = 'required'
    error_css_class = 'required'
    windfarm = forms.ModelMultipleChoiceField(queryset=WindFarm.objects.filter(available=True), widget=autocomplete.ModelSelect2Multiple(url='turbines:windfarm-autocomplete'), required=False)

    class Meta:
        model = Project
        form_tag = False
        fields = ('name', 'status', 'prob', 'turbines', 'customer', 'customer_contact', 'contract', 'contract_type', 'run_time', 'request_date', 'start_operation', 'contract_signature', 'price', 'ebt', 'dwt', 'sales_manager', 'offer_number')#, 'turbines__windfarm'
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
                    }

class CommentForm(forms.ModelForm):
    prefix = 'comment'
    required_css_class = 'required'
    error_css_class = 'required'
    class Meta:
        model = Comment
        form_tag = False
        fields = ('text','file')

class OfferNumberForm(forms.ModelForm):
    prefix = 'offer_number'
    required_css_class = 'required'
    error_css_class = 'required'

    class Meta:
        model = OfferNumber
        form_tag = False
        fields = ('number','wind_farm', 'amount', 'wec_typ', 'sales_manager', 'text')
        widgets = {'sales_manager': autocomplete.ModelSelect2(url='turbines:user-autocomplete'),
                    'wec_typ': autocomplete.ModelSelect2Multiple(url='turbines:wec-typ-autocomplete'),
                    'number': forms.TextInput(attrs={'readonly':'readonly'})}


class DrivingForm(forms.Form):
    distance = forms.FloatField(label="Distance [km]", widget=forms.NumberInput(attrs={'id': 'driving-distance'}))
    hours = forms.FloatField(label="Duration [min]", widget=forms.NumberInput(attrs={'id': 'driving-minutes'}))

class ContractsInCloseDistanceForm(forms.Form):
    distance = forms.FloatField(label="Distance [km]", widget=forms.NumberInput(attrs={'id': 'distance-number'}))
