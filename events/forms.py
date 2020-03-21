from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Event, Date
from wind_farms.models import WindFarm
from turbine.models import Turbine

from dal import autocomplete
from modeltranslation.forms import TranslationModelForm

class EventForm(TranslationModelForm):
    required_css_class = 'required'
    error_css_class = 'required'

    windfarm = forms.ModelMultipleChoiceField(queryset=WindFarm.objects.filter(available=True), widget=autocomplete.ModelSelect2Multiple(url='turbines:windfarm-autocomplete'), required=False, label=_("Wind Farm"))
    all_turbines = forms.BooleanField(label=_("All turbines of windfarm?"), required=False)
    turbines = forms.ModelMultipleChoiceField(queryset=Turbine.objects.filter(available=True), widget=autocomplete.ModelSelect2Multiple(url='turbines:turbineID-autocomplete', forward=['windfarm']), required=False, label=_("Turbines"))

    def clean(self):
        cleaned_data = super(EventForm, self).clean()
        if cleaned_data['all_turbines'] == True:
            turbines = Turbine.objects.filter(wind_farm__in=cleaned_data['windfarm'], available=True)
            cleaned_data['turbines'] = turbines
        return cleaned_data

    class Meta:
      model = Event
      form_tag = False
      fields = ('title', 'turbines', 'every_count', 'time_interval', 'for_count', 'duration', 'done', 'responsibles', 'all_turbines', 'part_of_contract')
      widgets = {'turbines': autocomplete.ModelSelect2Multiple(url='turbines:turbineID-autocomplete', forward=['windfarm']),
                'done': forms.DateInput(attrs={'type':'date'}),
                'responsibles': autocomplete.ModelSelect2Multiple(url='turbines:customer-relations-autocomplete'),}

class DateForm(forms.ModelForm):
    required_css_class = 'required'
    error_css_class = 'required'

    windfarm = forms.ModelMultipleChoiceField(queryset=WindFarm.objects.filter(available=True), widget=autocomplete.ModelSelect2Multiple(url='turbines:windfarm-autocomplete'), required=False, label=_("Wind Farm"))
    turbine = forms.ModelChoiceField(queryset=Turbine.objects.filter(available=True), widget=autocomplete.ModelSelect2(url='turbines:turbineID-autocomplete', forward=['windfarm']), required=False, label=_("Turbine"))
    next_dates_based_on_execution_date = forms.BooleanField(label=_("Calculation of next dates based on last execution date?"), required=False)
    next = forms.CharField(required=False)

    class Meta:
        model = Date
        form_tag = False
        fields = ('event', 'date', 'turbine', 'status', 'execution_date', 'service_provider', 'order_date', 'comment', 'next', 'next_dates_based_on_execution_date')#, 'part_of_contract'
        widgets = {'date': forms.DateInput(attrs={'type':'date'}),
                    'execution_date': forms.DateInput(attrs={'type':'date'}),
                    'order_date': forms.DateInput(attrs={'type':'date'}),
                    'turbine': autocomplete.ModelSelect2(url='turbines:turbineID-autocomplete', forward=['windfarm']),
                    'service_provider': autocomplete.ModelSelect2(url='turbines:actor-autocomplete'),}

class ChangeMultipleDatesForm(forms.ModelForm):
    required_css_class = 'required'
    error_css_class = 'required'

    dates = forms.ModelMultipleChoiceField(queryset=Date.objects.all(), widget=autocomplete.ModelSelect2Multiple(url='turbines:date-autocomplete'))

    def __init__(self, *args, **kwargs):
        event_pk = kwargs.pop('event_pk')
        super(ChangeMultipleDatesForm, self).__init__(*args, **kwargs)
        self.fields['dates'].initial = Date.objects.filter(event=event_pk)

    class Meta:
        model = Date
        form_tag = False
        fields = ('dates', 'status', 'execution_date', 'service_provider', 'order_date', 'comment')#, 'next_dates_based_on_execution_date') , 'part_of_contract'
        widgets = {'date': forms.DateInput(attrs={'type':'date'}),
                    'execution_date': forms.DateInput(attrs={'type':'date'}),
                    'order_date': forms.DateInput(attrs={'type':'date'}),
                    'service_provider': autocomplete.ModelSelect2(url='turbines:actor-autocomplete'),}