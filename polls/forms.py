from .models import WEC_Typ, Image
from projects.forms import HTML5RequiredMixin

from dal import autocomplete

from django import forms
from django.utils.translation import ugettext_lazy as _

class WEC_TypForm(HTML5RequiredMixin, forms.ModelForm):

    class Meta:
        model = WEC_Typ
        form_tag = False
        fields = ('name', 'manufacturer', 'output_power', 'rotor_diameter', 'wind_clas', 'year', 'reg', 'drive', 'offshore', 'tot_weight_t', 'hub_weight_t', 'tower_weight_t',
                'rotor_weight_t', 'min_rot_speed_r_m', 'max_rot_speed_r_m', 'cut_in', 'nominal_speed', 'cut_out', 'min_hub_height', 'max_hub_height', 'description', 'nr_blades',
                'product_web', 'produced_until', 'sound_level', 'serviced_by_dwt', 'maintenance_hours', 'technology_class')
        widgets = {'manufacturer': autocomplete.ModelSelect2(url='turbines:manufacturer-autocomplete'),
                    'product_web': forms.TextInput(attrs={'placeholder': 'http://deutsche-windtechnik.com'}),}
        labels = {'wind_clas': _('Wind Class'),
                    'manufacturer': _('Manufacturer'),
                    'output_power': _('Output Power'),
                    'rotor_diameter': _('Rotor Diameter'),
                    'year': _('Year'),
                    'tot_weight_t': _('Total Weight [t]'),
                    'hub_weight_t': _('Hub Heights [t]'),
                    'tower_weight_t': _('Tower Weight [t}'),}

class ImageForm(forms.ModelForm):
    required_css_class = 'required'
    error_css_class = 'required'
    agree = forms.BooleanField(required = True, error_messages={'required': _('Please verify the copyright of this picture')})

    class Meta:
        model = Image
        form_tag = False
        fields = ('file', 'source', 'description')
