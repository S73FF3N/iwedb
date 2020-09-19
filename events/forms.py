from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Event, Date, EVENTS
from wind_farms.models import WindFarm
from turbine.models import Turbine
from projects.forms import HTML5RequiredMixin

from dal import autocomplete
#from modeltranslation.forms import TranslationModelForm

TOWER = (
    ('Lattice Tower', _('Lattice Tower')),
    ('Tubular Tower', _('Tubular Tower')),
    ('Hybrid', _('Hybrid')),
    )

ALARM_SYSTEM = (
    ('Yes', _('Yes')),
    ('No', _('No')),
    ('No information', _('No information')),
    )

class EventForm(HTML5RequiredMixin, forms.ModelForm):

    windfarm = forms.ModelMultipleChoiceField(queryset=WindFarm.objects.filter(available=True), widget=autocomplete.ModelSelect2Multiple(url='turbines:windfarm-autocomplete'), required=False, label=_("Wind Farm"))
    all_turbines = forms.BooleanField(label=_("All turbines of windfarm?"), required=False)
    turbines = forms.ModelMultipleChoiceField(queryset=Turbine.objects.filter(available=True), widget=autocomplete.ModelSelect2Multiple(url='turbines:turbineID-autocomplete', forward=['windfarm']), label=_("Turbines"))

    def clean(self):
        cleaned_data = super(EventForm, self).clean()
        if cleaned_data['all_turbines'] == True:
            turbines = Turbine.objects.filter(wind_farm__in=cleaned_data['windfarm'], available=True)
            cleaned_data['turbines'] = turbines
        return cleaned_data

    class Meta:
      model = Event
      form_tag = False
      fields = ('title', 'windfarm', 'turbines', 'every_count', 'time_interval', 'for_count', 'duration', 'done', 'responsibles', 'all_turbines', 'part_of_contract')
      widgets = {'turbines': autocomplete.ModelSelect2Multiple(url='turbines:turbineID-autocomplete', forward=['windfarm']),
                'done': forms.DateInput(attrs={'type':'date'}),
                'responsibles': autocomplete.ModelSelect2Multiple(url='turbines:customer-relations-autocomplete'),}

class DateForm(HTML5RequiredMixin, forms.ModelForm):

    def __init__(self, initial=None, *args, **kwargs):
        super (DateForm,self ).__init__(*args,**kwargs)
        try:
            self.fields['turbine'].queryset = initial['event'].turbines.all()
            #self.fields['turbine'].widget = autocomplete.ModelSelect2(url='turbines:turbineID-autocomplete', forward=(forward.Const(initial['event'].id, 'event_id')))
        except:
            self.fields['turbine'].queryset = Turbine.objects.filter(available=True)

    windfarm = forms.ModelMultipleChoiceField(queryset=WindFarm.objects.filter(available=True), widget=autocomplete.ModelSelect2Multiple(url='turbines:windfarm-autocomplete'), required=False, label=_("Wind Farm"))
    turbine = forms.ModelChoiceField(queryset=None, required=False, label=_("Turbine"))
    next_dates_based_on_execution_date = forms.BooleanField(label=_("Calculation of next dates based on last execution date?"), required=False)
    next = forms.CharField(required=False)

    class Meta:
        model = Date
        form_tag = False
        fields = ('date', 'windfarm', 'turbine', 'status', 'execution_date', 'service_provider', 'order_date', 'comment', 'next', 'next_dates_based_on_execution_date')#, 'part_of_contract'
        widgets = {'date': forms.DateInput(attrs={'type':'date'}),
                    'execution_date': forms.DateInput(attrs={'type':'date'}),
                    'order_date': forms.DateInput(attrs={'type':'date'}),
                    'service_provider': autocomplete.ModelSelect2(url='turbines:actor-autocomplete'),}

class DateFilterForm(forms.Form):

    date_start = forms.DateField(label=_("Between"),  widget=forms.DateInput(attrs={'type':'date'}))
    date_end = forms.DateField(label=_("And"), widget=forms.DateInput(attrs={'type':'date'}))

class ChangeAllDatesForm(HTML5RequiredMixin, forms.ModelForm):

    dates = forms.ModelMultipleChoiceField(queryset=Date.objects.all(), widget=autocomplete.ModelSelect2Multiple(url='turbines:date-autocomplete'))
    next_dates_based_on_execution_date = forms.BooleanField(label=_("Calculation of next dates based on last execution date?"), required=False)

    def __init__(self, *args, **kwargs):
        event_pk = kwargs.pop('event_pk')
        super(ChangeAllDatesForm, self).__init__(*args, **kwargs)
        self.fields['dates'].initial = Date.objects.filter(event=event_pk)

    class Meta:
        model = Date
        form_tag = False
        fields = ('dates', 'status', 'execution_date', 'service_provider', 'order_date', 'comment')#, 'next_dates_based_on_execution_date')# , 'part_of_contract'
        widgets = {'date': forms.DateInput(attrs={'type':'date'}),
                    'execution_date': forms.DateInput(attrs={'type':'date'}),
                    'order_date': forms.DateInput(attrs={'type':'date'}),
                    'service_provider': autocomplete.ModelSelect2(url='turbines:actor-autocomplete'),}

class ChangeMultipleDatesForm(HTML5RequiredMixin, forms.ModelForm):

    dates = forms.ModelMultipleChoiceField(queryset=Date.objects.all(), widget=autocomplete.ModelSelect2Multiple(url='turbines:date-autocomplete'))
    next_dates_based_on_execution_date = forms.BooleanField(label=_("Calculation of next dates based on last execution date?"), required=False)

    def __init__(self, *args, **kwargs):
        dates = kwargs.pop('dates')
        event_pk = kwargs.pop('event_pk')
        super(ChangeMultipleDatesForm, self).__init__(*args, **kwargs)
        self.fields['dates'].initial = Date.objects.filter(event=event_pk).filter(id__in=dates)

    class Meta:
        model = Date
        form_tag = False
        fields = ('dates', 'status', 'execution_date', 'service_provider', 'order_date', 'comment', 'next_dates_based_on_execution_date') #, 'part_of_contract'
        widgets = {'date': forms.DateInput(attrs={'type':'date'}),
                    'execution_date': forms.DateInput(attrs={'type':'date'}),
                    'order_date': forms.DateInput(attrs={'type':'date'}),
                    'service_provider': autocomplete.ModelSelect2(url='turbines:actor-autocomplete'),}

class CreateOrderForm(HTML5RequiredMixin, forms.Form):

    #Order form
    order_no = forms.IntegerField(label=_("Order number"), min_value=0, required=False)
    recipient = forms.CharField(label=_("Recipient"), required=False)
    order_date = forms.DateField(label=_("Order date"), widget=forms.DateInput(attrs={'type':'date'}), required=False)
    ordered_by = forms.CharField(label=_("Ordered by"), widget=forms.Textarea, required=False)

    wind_farm_desc = forms.CharField(label=_("Description"), required=False)
    wind_farm_wec_count = forms.IntegerField(label=_("Amount of Turbines"), min_value=0, required=False)
    wind_farm_wka = forms.CharField(label=_("Turbine ID"), required=False)

    event_type = forms.ChoiceField(label=_("Type"), choices=EVENTS, required=False)

    price = forms.FloatField(label=_("Price"), min_value=0, required=False)

    date_request = forms.IntegerField(label=_("Calendar week"), min_value=0, required=False)
    date_asap = forms.BooleanField(label=_("asap"), required=False)

    documents = forms.CharField(label=_("Reports & invoices to:"), required=False)

    customer_manager = forms.CharField(label=_("Customer Relationship Responsible"), required=False)

    #Order confirmation
    order_accepted = forms.DateField(label=_("Order accepted on"), widget=forms.DateInput(attrs={'type':'date'}), required=False)
    planned_execution = forms.DateField(label=_("Execution planned on"), widget=forms.DateInput(attrs={'type':'date'}), required=False)
    name = forms.CharField(label=_("Name"), required=False)
    confirmation_comment = forms.CharField(label=_("Comment"), widget=forms.Textarea, required=False)

    #Wind farm location information
    postcode = forms.IntegerField(label=_("Postal Code"), min_value=0, required=False)
    location = forms.CharField(label=_("Location"), required=False)
    address = forms.CharField(label=_("Address"), required=False)

    wec_manufacturer = forms.CharField(label=_("Manufacturer"), required=False)
    wec_type = forms.CharField(label=_("Type"), required=False)
    rotor_blade_type = forms.CharField(label=_("Rotor Blades"), required=False)
    rated_capacity = forms.CharField(label=_("Output Power"), required=False)
    hub_height = forms.CharField(label=_("Hub Height"), required=False)
    wec_count = forms.IntegerField(label=_("Amount of Turbines"), min_value=0, required=False)
    serials = forms.CharField(label=_("Turbine ID"), required=False)
    tower_type = forms.ChoiceField(label=_("Type"), choices=TOWER, required=False)
    service_lift = forms.BooleanField(label=_("Service Lift"), required=False)
    service_lift_manufacturer = forms.CharField(label=_("Service lift manufacturer"), required=False)
    winch = forms.CharField(label=_("Winch"), required=False)
    bso = forms.CharField(label=_("BSO"), required=False)
    fall_protection_system = forms.CharField(label=_("Fall protection system"), required=False)
    local_runner = forms.BooleanField(label=_("Arrester available"), required=False)

    contact_person = forms.CharField(label=_("Contact Person"), required=False)
    contact_person_tel = forms.CharField(label=_("Phone"), required=False)
    contact_person_address = forms.CharField(label=_("Address"), required=False)
    key = forms.CharField(label=_("Key"), required=False)
    key_code = forms.CharField(label=_("Key Safe Code"), required=False)
    alarm_system = forms.ChoiceField(label=_("Alarm System"), choices=ALARM_SYSTEM, required=False)

    company = forms.CharField(label=_("Company"), required=False)
    company_contact_person = forms.CharField(label=_("Contact person"), required=False)
    company_tel = forms.CharField(label=_("Phone"), required=False)

    sp_report = forms.BooleanField(label=_("SP report submitted"), required=False)
    direction_report = forms.BooleanField(label=_("Direction report submitted"), required=False)

    miscellaneous = forms.CharField(label=_("Miscellaneous"), widget=forms.Textarea, required=False)

    #other
    date = forms.DateField(label=_("Date"), widget=forms.DateInput(attrs={'type':'date'}), required=False)
