from django import forms

from .models import Project, Comment

from dal import autocomplete

class ProjectForm(forms.ModelForm):
    prefix = 'project'

    class Meta:
        model = Project
        form_tag = False
        fields = ('name', 'status', 'prob', 'turbines', 'customer', 'new_customer', 'customer_contact', 'last_contact', 'contract_type', 'run_time', 'department', 'responsible', 'request_date', 'start_operation', 'contract_signature', 'price', 'ebt', 'dwt')
        widgets = {'turbines': autocomplete.ModelSelect2Multiple(url='turbines:turbineID-autocomplete'),
                    'customer': autocomplete.ModelSelect2(url='turbines:actor-autocomplete'),
                    'customer_contact': autocomplete.ModelSelect2(url='turbines:person-autocomplete', forward=['customer']),
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
