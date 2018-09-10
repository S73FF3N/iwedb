from django import forms
from .models import Player, Person
from dal import autocomplete

class PlayerForm(forms.ModelForm):

    class Meta:
        model = Player
        form_tag = False
        fields = ('name', 'country', 'city', 'adress', 'postal_code', 'phone', 'mail', 'web', 'sector', 'customer_code')
        widgets = {'country': autocomplete.ModelSelect2(url='turbines:country-autocomplete')}
        error_messages = {'sector' : {'required' : "Select at least one sector!",},}

class PersonForm(forms.ModelForm):

    class Meta:
        model = Person
        fields = ('name', 'function', 'phone', 'phone2', 'mail')
        widgets = {'company': autocomplete.ModelSelect2Multiple(url='turbines:actor-autocomplete'),}

class PersonEditForm(forms.ModelForm):

    class Meta:
        model = Person
        fields = ('name', 'company', 'function', 'phone', 'phone2', 'mail')
        widgets = {'company': autocomplete.ModelSelect2Multiple(url='turbines:actor-autocomplete'),}