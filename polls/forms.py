from .models import WEC_Typ, Image
from django import forms
from dal import autocomplete

class WEC_TypForm(forms.ModelForm):

    class Meta:
        model = WEC_Typ
        form_tag = False
        fields = ('name', 'manufacturer', 'output_power', 'rotor_diameter', 'year', 'wind_class', 'reg', 'drive', 'offshore', 'tot_weight_t', 'hub_weight_t', 'tower_weight_t',
                'rotor_weight_t', 'min_rot_speed_r_m', 'max_rot_speed_r_m', 'cut_in', 'nominal_speed', 'cut_out', 'min_hub_height', 'max_hub_height', 'description', 'nr_blades', 'product_web', 'produced_until') #  'image',
        widgets = {'manufacturer': autocomplete.ModelSelect2(url='turbines:manufacturer-autocomplete')}

class ImageForm(forms.ModelForm):

    class Meta:
        model = Image
        form_tag = False
        fields = ('file', 'source', 'description')#, 'name', 'content_type', 'object_id')
