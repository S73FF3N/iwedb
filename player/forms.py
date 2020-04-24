from django import forms

from .models import Player, Person, File
from django.utils.translation import ugettext_lazy as _

from dal import autocomplete

class PlayerForm(forms.ModelForm):
    required_css_class = 'required'
    error_css_class = 'required'
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

class PersonForm(forms.ModelForm):
    required_css_class = 'required'
    error_css_class = 'error'
    class Meta:
        model = Person
        fields = ('name', 'function', 'phone', 'phone2', 'mail', 'adress', 'city', 'postal_code')
        widgets = {'company': autocomplete.ModelSelect2Multiple(url='turbines:actor-autocomplete'),
                    'phone': forms.TextInput(attrs={'placeholder': '+49 54138 05 38 100'}),
                    'phone2': forms.TextInput(attrs={'placeholder': '+49 54138 05 38 100'}),
                    'mail': forms.TextInput(attrs={'placeholder': 'info@deutsche-windtechnik.com'}),}
        labels = {'phone2': _('Alternative Phone'),
                    'adress': _('Address'),
                    'function': _('Function'),
                    'phone': _('Phone'),
                    'mail': _('Mail'),
                    'city': _('City'),
                    'postal_code': _('Postal Code'),}

class PersonEditForm(forms.ModelForm):
    required_css_class = 'required'
    error_css_class = 'required'
    class Meta:
        model = Person
        fields = ('name', 'company', 'function', 'phone', 'phone2', 'mail', 'adress', 'city', 'postal_code')
        widgets = {'company': autocomplete.ModelSelect2Multiple(url='turbines:actor-autocomplete'),
                    'phone': forms.TextInput(attrs={'placeholder': '+49 54138 05 38 100'}),
                    'phone2': forms.TextInput(attrs={'placeholder': '+49 54138 05 38 100'}),
                    'mail': forms.TextInput(attrs={'placeholder': 'info@deutsche-windtechnik.com'}),}
        labels = {'company': _('Company'),
                    'function': _('Function'),
                    'phone': _('Phone'),
                    'phone2': _('Alternative Phone'),
                    'adress': _('Adress'),
                    'city': _('City'),
                    'postal_code': _('Postal Code'),}

class FileForm(forms.ModelForm):
    prefix = 'file'
    required_css_class = 'required'
    error_css_class = 'required'
    class Meta:
        model = File
        form_tag = False
        fields = ('name', 'file')