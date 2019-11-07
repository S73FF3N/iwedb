from django import forms

from .models import Event, Date
from wind_farms.models import WindFarm
from turbine.models import Turbine

from dal import autocomplete

class EventForm(forms.ModelForm):
    required_css_class = 'required'
    error_css_class = 'required'

    windfarm = forms.ModelMultipleChoiceField(queryset=WindFarm.objects.filter(available=True), widget=autocomplete.ModelSelect2Multiple(url='turbines:windfarm-autocomplete'), required=False, label="Windpark")
    turbines = forms.ModelMultipleChoiceField(queryset=Turbine.objects.filter(available=True), widget=autocomplete.ModelSelect2Multiple(url='turbines:turbineID-autocomplete', forward=['windfarm']), required=False, label="WEA")

    class Meta:
      model = Event
      form_tag = False
      fields = ('title', 'turbines', 'every_count', 'time_interval', 'for_count', 'duration', 'done', 'responsible')
      widgets = {'turbines': autocomplete.ModelSelect2Multiple(url='turbines:turbineID-autocomplete', forward=['windfarm']),
                'done': forms.DateInput(attrs={'placeholder': '2020-12-31'}),
                'responsible': autocomplete.ModelSelect2(url='turbines:technical-operations-autocomplete'),}

class DateForm(forms.ModelForm):
    required_css_class = 'required'
    error_css_class = 'required'

    windfarm = forms.ModelMultipleChoiceField(queryset=WindFarm.objects.filter(available=True), widget=autocomplete.ModelSelect2Multiple(url='turbines:windfarm-autocomplete'), required=False, label="Windpark")
    turbine = forms.ModelChoiceField(queryset=Turbine.objects.filter(available=True), widget=autocomplete.ModelSelect2(url='turbines:turbineID-autocomplete', forward=['windfarm']), required=False, label="WEA")
    next = forms.CharField(required=False)

    class Meta:
        model = Date
        form_tag = False
        fields = ('event', 'date', 'turbine', 'status', 'execution_date', 'service_provider', 'comment', 'part_of_contract', 'next')
        widgets = {'date': forms.DateInput(),
                    'turbine': autocomplete.ModelSelect2(url='turbines:turbineID-autocomplete', forward=['windfarm']),
                    'execution_date': forms.DateInput(),
                    'service_provider': autocomplete.ModelSelect2(url='turbines:actor-autocomplete'),}