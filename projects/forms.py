from django import forms

from .models import Project, Comment
from wind_farms.models import WindFarm

from dal import autocomplete

class ProjectForm(forms.ModelForm):
    prefix = 'project'

    windfarm = forms.ModelMultipleChoiceField(queryset=WindFarm.objects.filter(available=True), widget=autocomplete.ModelSelect2Multiple(url='turbines:windfarm-autocomplete'), required=False)

    class Meta:
        model = Project
        form_tag = False
        fields = ('name', 'status', 'prob', 'turbines', 'customer', 'new_customer', 'customer_contact', 'contract_type', 'run_time', 'department', 'request_date', 'start_operation', 'contract_signature', 'price', 'ebt', 'dwt', 'sales_manager', 'offer_nr')#, 'turbines__windfarm'
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
                    }

class CommentForm(forms.ModelForm):
    prefix = 'comment'

    class Meta:
        model = Comment
        form_tag = False
        fields = ('text','file')

class DrivingForm(forms.Form):
    distance = forms.FloatField(label="Distance [km]")
    hours = forms.FloatField(label="Duration [min]")

class ContractsInCloseDistanceForm(forms.Form):
    distance = forms.FloatField(label="Distance [km]")
