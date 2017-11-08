from .models import Gearbox, Generator, Tower
from django import forms
from dal import autocomplete

class GearboxForm(forms.ModelForm):
    class Meta:
        model = Gearbox
        form_tag = False
        fields = ('name', 'manufacturer', 'weight_t', 'compatible_to', 'ratio', 'stages')
        widgets = {'compatible_to': autocomplete.ModelSelect2(url='turbines:wec-typ-autocomplete')}

class GeneratorForm(forms.ModelForm):
    class Meta:
        model = Generator
        form_tag = False
        fields = ('name', 'manufacturer', 'weight_t', 'compatible_to', 'voltage', 'rpm', 'generator_type')
        widgets = {'compatible_to': autocomplete.ModelSelect2(url='turbines:wec-typ-autocomplete')}

class TowerForm(forms.ModelForm):
    class Meta:
        model = Tower
        form_tag = False
        fields = ('name', 'manufacturer', 'weight_t', 'compatible_to', 'tower_type')
        widgets = {'compatible_to': autocomplete.ModelSelect2(url='turbines:wec-typ-autocomplete')}