from django import forms
from .models import Player, Person

from dal import autocomplete

class PlayerForm(forms.ModelForm):
    required_css_class = 'required'
    error_css_class = 'required'
    class Meta:
        model = Player
        form_tag = False
        fields = ('name', 'country', 'city', 'adress', 'postal_code', 'phone', 'mail', 'web', 'sector')#, 'customer_code')
        widgets = {'country': autocomplete.ModelSelect2(url='turbines:country-autocomplete'),
                    'phone': forms.TextInput(attrs={'placeholder': '+49 54138 05 38 100'}),
                    'mail': forms.TextInput(attrs={'placeholder': 'info@deutsche-windtechnik.com'}),
                    'web': forms.TextInput(attrs={'placeholder': 'http://deutsche-windtechnik.com'}),}
        error_messages = {'sector' : {'required' : "Select at least one sector!",},}

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