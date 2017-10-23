from .models import Component
from django import forms

class ComponentForm(forms.ModelForm):
    class Meta:
        model = Component
        form_tag = False
        fields = ('name', 'manufacturer', 'component_type', 'weight_t', 'image', 'compatible_to')