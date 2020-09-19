from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Player, Person, File, MailingList
from projects.forms import HTML5RequiredMixin

from dal import autocomplete

class PlayerForm(HTML5RequiredMixin, forms.ModelForm):
    class Meta:
        model = Player
        form_tag = False
        fields = ('name', 'country', 'city', 'adress', 'postal_code', 'phone', 'mail', 'web', 'sector', 'head_organisation')
        widgets = {'name': forms.TextInput(attrs={'id': 'actor-name'}),
                    'country': autocomplete.ModelSelect2(url='turbines:country-autocomplete'),
                    'phone': forms.TextInput(attrs={'placeholder': '+49 54138 05 38 100'}),
                    'mail': forms.TextInput(attrs={'placeholder': 'info@deutsche-windtechnik.com'}),
                    'web': forms.TextInput(attrs={'placeholder': 'http://deutsche-windtechnik.com'}),
                    'head_organisation': autocomplete.ModelSelect2(url='turbines:actor-autocomplete'),}
        error_messages = {'sector' : {'required' : "Select at least one sector!",},}
        labels = {'country': _('Country'),
                    'city': _('City'),
                    'adress': _('Adress'),
                    'postal_code': _('Postal Code'),
                    'phone': _('Phone'),
                    'mail': _('Mail'),
                    'sector': _('Sector'),
                    'head_organisation': _('Head Organisation'),}

class PersonForm(HTML5RequiredMixin, forms.ModelForm):
    mailing_list = forms.ModelMultipleChoiceField(queryset=MailingList.objects.all(), widget=forms.CheckboxSelectMultiple(), required=False)
    class Meta:
        model = Person
        fields = ('gender', 'first_name', 'name', 'function', 'phone', 'phone2', 'mail', 'adress', 'city', 'postal_code', 'country', 'postal_communication', 'mailing_list')
        widgets = {'company': autocomplete.ModelSelect2Multiple(url='turbines:actor-autocomplete'),
                    'phone': forms.TextInput(attrs={'placeholder': '+49 54138 05 38 100'}),
                    'phone2': forms.TextInput(attrs={'placeholder': '+49 54138 05 38 100'}),
                    'mail': forms.TextInput(attrs={'placeholder': 'info@deutsche-windtechnik.com'}),
                    'country': autocomplete.ModelSelect2(url='turbines:country-autocomplete'),}
        labels = {'phone2': _('Alternative Phone'),
                    'adress': _('Address'),
                    'function': _('Function'),
                    'phone': _('Phone'),
                    'mail': _('Mail'),
                    'city': _('City'),
                    'postal_code': _('Postal Code'),
                    'gender': _("Gender"),
                    'first_name': _("First Name"),
                    'last_name': _("Last Name"),
                    'mailing_list': _("Mailing list")}

class PersonEditForm(HTML5RequiredMixin, forms.ModelForm):
    mailing_list = forms.ModelMultipleChoiceField(queryset=MailingList.objects.all(), widget=forms.CheckboxSelectMultiple(), required=False)
    class Meta:
        model = Person
        fields = ('gender', 'first_name', 'name', 'company', 'function', 'phone', 'phone2', 'mail', 'adress', 'city', 'postal_code', 'country', 'postal_communication', 'mailing_list')
        widgets = {'company': autocomplete.ModelSelect2Multiple(url='turbines:actor-autocomplete'),
                    'phone': forms.TextInput(attrs={'placeholder': '+49 54138 05 38 100'}),
                    'phone2': forms.TextInput(attrs={'placeholder': '+49 54138 05 38 100'}),
                    'mail': forms.TextInput(attrs={'placeholder': 'info@deutsche-windtechnik.com'}),
                    'country': autocomplete.ModelSelect2(url='turbines:country-autocomplete'),}
        labels = {'company': _('Company'),
                    'function': _('Function'),
                    'phone': _('Phone'),
                    'phone2': _('Alternative Phone'),
                    'adress': _('Adress'),
                    'city': _('City'),
                    'postal_code': _('Postal Code'),}

class FileForm(HTML5RequiredMixin, forms.ModelForm):
    prefix = 'file'
    class Meta:
        model = File
        form_tag = False
        fields = ('name', 'file')
