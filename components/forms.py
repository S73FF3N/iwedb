from .models import Component
from django import forms
from dal import autocomplete

class ComponentForm(forms.ModelForm):
    class Meta:
        model = Component
        form_tag = False
        fields = ('name', 'manufacturer', 'component_type', 'weight_t', 'image', 'compatible_to')
        widgets = {'compatible_to': autocomplete.ModelSelect2Multiple(url='turbines:wec-typ-autocomplete')}