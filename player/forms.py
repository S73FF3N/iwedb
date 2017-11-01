from django import forms
from .models import Player
from dal import autocomplete

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        form_tag = False
        fields = ('name', 'country', 'city', 'adress', 'postal_code', 'phone', 'mail', 'web', 'sector')
        widgets = {'country': autocomplete.ModelSelect2(url='turbines:country-autocomplete')}