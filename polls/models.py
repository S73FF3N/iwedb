from jsonfield import JSONField

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields
from django.utils.translation import gettext_lazy as _

from turbine.models import Turbine, Contract

OFFSHORE = (
    ('yes', _('yes')),
    ('no', _('no')),)

REGULATION = (
    ('pitch', 'pitch'),
    ('stall', 'stall'),)

DRIVE = (
    ('gearbox', _('gearbox')),
    ('gearless', _('gearless')),)

SERVICED_BY_DWT = (
    ('No', _('No')),
    ('Basic', 'Basic'),
    ('Full Service', _('Full Service')),)

TECHNOLOGY_CLASS = (
    ('MD', 'MD'),
    ('FL2500', 'FL2500'),
    ('MM', 'MM'),
    ('3.XM', '3.XM'),
    ('3.XM NES', '3.XM NES'),
    ('3.XM EBC', '3.XM EBC'),
    ('N60', 'N60'),
    ('N80/90', 'N80/90'),
    ('gamma', 'gamma'),
    ('delta', 'delta'),
    ('delta4000', 'delta4000'),
    ('5M', '5M'),
    )

class Wind_Class(models.Model):
    name = models.CharField(max_length=20, db_index=True)

    def __str__(self):
        return self.name

class Image(models.Model):
    name = models.CharField(max_length=50, db_index=True, default="wind turbine name")
    file = models.ImageField(blank=True, upload_to='wec_types/%Y/%m/%d', help_text=_("Upload an image file (jpg or png)"), verbose_name=_("File"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    source = models.CharField(max_length=200, help_text=_("State the source/owner of the image"), verbose_name=_("Source"))

    limit = models.Q(app_label = 'polls', model = 'wec_typ') | models.Q(app_label = 'wind_farms', model = 'windfarm') | models.Q(app_label = 'turbine', model = 'turbine')
    content_type = models.ForeignKey(ContentType, limit_choices_to = limit, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = fields.GenericForeignKey('content_type', 'object_id')

    created = models.DateTimeField(auto_now_add=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'manufacturer'
        verbose_name_plural = 'manufacturers'

    def __str__(self):
        return self.name


class WEC_Typ(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, related_name='wec_types', verbose_name=_("Manufacturer"))
    name = models.CharField(max_length=200, db_index=True, help_text=_("Name of the turbine model"))
    slug = models.SlugField(max_length=200, db_index=True)
    technology_class = models.CharField(max_length=25, choices=TECHNOLOGY_CLASS, null=True, blank=True, verbose_name=_('Technology Class'))
    image = fields.GenericRelation(Image, related_query_name='images')
    description = models.TextField(blank=True, help_text=_("Additional information"), verbose_name=_("Description"))
    serviced_by_dwt = models.CharField(max_length=20, choices=SERVICED_BY_DWT, default='No', verbose_name=_('Serviced by DWT'))
    maintenance_hours = models.IntegerField(blank=True, null=True, help_text=_("How many maintenance hours have to be substracted from the availability guarantee?"), verbose_name=_("Maintenance Hours"))

    output_power = models.IntegerField(blank=True, null=True, verbose_name=_('Output power'), help_text=_("Enter rated output power in kW"))
    rotor_diameter = models.IntegerField(blank=True, null=True, verbose_name=_('Rotor diameter'), help_text=_("Enter rotor diameter in m"))
    nr_blades = models.IntegerField(default=3, blank=True, null=True, verbose_name=_('Amount of blades'))
    wind_clas = models.ManyToManyField('Wind_Class', help_text=_("Select (multiple) wind class"), blank=True, verbose_name=_("Wind Class"))
    year = models.IntegerField(blank=True, null=True, verbose_name=_('First installation'), help_text=_("In which year was this turbine model built first?"))
    offshore = models.CharField(max_length=20, choices=OFFSHORE, default='no', help_text=_("Is this turbine model built for offshore?"))
    reg = models.CharField(max_length=20, choices=REGULATION, default='pitch', verbose_name=_('Regulation'))
    drive = models.CharField(max_length=20, choices=DRIVE, default='gearbox', verbose_name=_('Drivetrain'))

    tot_weight_t = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name=_('Total weight [t]'))
    tower_weight_t = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name=_('Tower weight [t]'))
    hub_weight_t = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name=_('Nacelle weight [t]'))
    rotor_weight_t = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name=_('Rotor weight [t]'))
    min_rot_speed_r_m = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name=_('Min. rotor speed [r/m]'))
    max_rot_speed_r_m = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name=_('Max. rotor speed [r/m]'))
    cut_in = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name=_('Cut in wind speed [m/s]'))
    nominal_speed = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name=_('Nominal wind speed [m/s]'))
    cut_out = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name=_('Cut out wind speed [m/s]'))
    min_hub_height = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name=_('Min. Hub Height [m]'))
    max_hub_height = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name=_('Max. Hub Height [m]'))
    sound_level = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, verbose_name=_("Sound level [dB]"))
    produced_until = models.IntegerField(blank=True, null=True, help_text=_("In which year was this turbine model built last?"), verbose_name=_("Produced until"))
    product_web = models.URLField(max_length=200, blank=True, verbose_name=_('Product web page'), help_text=_("Link to more information"))
    comment = fields.GenericRelation('projects.Comment')

    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, db_index=True)

    power_curve = JSONField(blank=True, null=True)

    def get_power_curve_data(self):
        data = []
        for i in self.power_curve["wind_speed"]:
            data.append([i])
        for idx, j in enumerate(self.power_curve["output_power"], start=0):
            data[idx].append(j)
        data.insert(0, ['Wind Speed', 'Output Power'])
        return data

    def turbine_of_type(self):
        wf = Turbine.objects.filter(wec_typ__name__exact=self.name, wec_typ__manufacturer__name=self.manufacturer, available=True)
        return wf

    def turbine_of_type_under_contract(self):
        turbines = Contract.objects.filter(turbines__wec_typ=self, active=True).values_list('turbines', flat=True)
        turbine_links = {}
        for t in turbines:
            try:
                turbine = Turbine.objects.get(pk=t)
                turbine_links[turbine.turbine_id] = turbine.get_absolute_url()
            except:
                pass
        return turbine_links

    def _amount_turbine_of_type_under_contract(self):
        turbines = Contract.objects.filter(turbines__wec_typ=self, active=True).values_list('turbines', flat=True)
        turbine_links = {}
        for t in turbines:
            try:
                turbine = Turbine.objects.get(pk=t)
                turbine_links[turbine.turbine_id] = turbine.get_absolute_url()
            except:
                pass
        return len(turbine_links)
    amount_turbine_of_type_under_contract = property(_amount_turbine_of_type_under_contract)

    def swept_area(self):
        sw_ar = round(3.1416 * (self.rotor_diameter^2)/4, 2)
        return sw_ar

    def power_density(self):
        p_den = round(self.output_power/self.rotor_diameter, 2)
        return p_den

    def all_comments(self):
        comments = self.comment.exclude(text__in=['created Turbine Type', 'edited Turbine Type'])
        return comments

    class Meta:
        ordering = ('-updated',)
        index_together = (('id', 'slug'),)
        permissions = (("comment", "Can comment on turbine models"),)

    def __str__(self):
        space = " "
        print_wec_type = self.manufacturer.name + space + self.name
        return print_wec_type

    def get_absolute_url(self):
        return reverse('polls:wec_typ_detail', args=[self.id, self.slug])

