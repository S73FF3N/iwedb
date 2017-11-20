from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields

from turbine.models import Turbine
from multiselectfield import MultiSelectField
from jsonfield import JSONField

OFFSHORE = (
    ('yes', 'yes'),
    ('no', 'no'),)

REGULATION = (
    ('pitch', 'pitch'),
    ('stall', 'stall'),)

DRIVE = (
    ('gearbox', 'gearbox'),
    ('gearless', 'gearless'),)

IECIA = 'Ia'
IECIB = 'Ib'
IECIIA = 'IIa'
IECIIB = 'IIb'
IECIIIA = 'IIIa'
IECIIIB = 'IIIb'
IECS = 'S'
IECIV = 'IV'

WIND_CLASS = (
    (IECIA, 'IEC Ia'),
    (IECIB, 'IEC Ib'),
    (IECIIA, 'IEC IIa'),
    (IECIIB, 'IEC IIb'),
    (IECIIIA, 'IEC IIIa'),
    (IECIIIB, 'IEC IIIb'),
    (IECS, 'IEC S'),
    (IECIV, 'IEC IV'))

class Image(models.Model):
    name = models.CharField(max_length=50, db_index=True, default="wind turbine name")
    file = models.ImageField(null=True, upload_to='wec_types/%Y/%m/%d')
    description = models.TextField(blank=True, null=True)
    source = models.CharField(max_length=200)

    limit = models.Q(app_label = 'polls', model = 'wec_typ') | models.Q(app_label = 'wind_farms', model = 'windfarm') | models.Q(app_label = 'components') | models.Q(app_label = 'turbine', model = 'turbine')
    content_type = models.ForeignKey(ContentType, limit_choices_to = limit, null=True, blank=True,)
    object_id = models.PositiveIntegerField(null=True,)
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

    def get_absolute_url(self):
        return reverse('polls:wec_typ_list_by_manufacturer', args=[self.slug])

class WEC_Typ(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, related_name='wea_types')
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = fields.GenericRelation(Image)
    description = models.TextField(blank=True, null=True)
    output_power = models.IntegerField(default=0, blank=True, null=True, verbose_name='Output power [kW]')
    rotor_diameter = models.IntegerField(default=0, blank=True, null=True, verbose_name='Rotor diameter [m]')
    nr_blades = models.IntegerField(default=3, blank=True, null=True, verbose_name='Amount of blades')
    wind_class = MultiSelectField(choices=WIND_CLASS, max_length=30, blank=True, null=True, default=IECIA)
    year = models.IntegerField(default=2000, blank=True, null=True, verbose_name='First installation')
    offshore = models.CharField(max_length=20, choices=OFFSHORE, default='no')
    reg = models.CharField(max_length=20, choices=REGULATION, default='pitch', verbose_name='Regulation')
    drive = models.CharField(max_length=20, choices=DRIVE, default='gearbox', verbose_name='Drivetrain')
    tot_weight_t = models.DecimalField(max_digits=6, decimal_places=2, default=400, blank=True, null=True, verbose_name='Total weight [t]')
    tower_weight_t = models.DecimalField(max_digits=6, decimal_places=2, default=250, blank=True, null=True, verbose_name='Tower weight [t]')
    hub_weight_t = models.DecimalField(max_digits=6, decimal_places=2, default=100, blank=True, null=True, verbose_name='Nacelle weight [t]')
    rotor_weight_t = models.DecimalField(max_digits=6, decimal_places=2, default=50, blank=True, null=True, verbose_name='Rotor weight [t]')
    min_rot_speed_r_m = models.DecimalField(max_digits=5, decimal_places=2, default=11.5, blank=True, null=True, verbose_name='Min. rotor speed [m/s]')
    max_rot_speed_r_m = models.DecimalField(max_digits=5, decimal_places=2, default=20.5, blank=True, null=True, verbose_name='Max. rotor speed [m/s]')
    cut_in = models.DecimalField(max_digits=5, decimal_places=2, default=3.5, blank=True, null=True, verbose_name='Cut in wind speed')
    nominal_speed = models.DecimalField(max_digits=5, decimal_places=2, default=15.0, blank=True, null=True, verbose_name='Nominal wind speed')
    cut_out = models.DecimalField(max_digits=5, decimal_places=2, default=25.0, blank=True, null=True, verbose_name='Cut out wind speed')
    min_hub_height = models.DecimalField(max_digits=6, decimal_places=2, default=60, blank=True, null=True, verbose_name='Min. Hub Height')
    max_hub_height = models.DecimalField(max_digits=6, decimal_places=2, default=140, blank=True, null=True, verbose_name='Max. Hub Height')
    produced_until = models.IntegerField(blank=True, null=True)
    product_web = models.URLField(max_length=200, blank=True, null=True, verbose_name='Product web page')
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    power_curve = JSONField(null=True, blank=True)

    def get_power_curve_data(self):
        data = []
        for i in self.power_curve["wind_speed"]:
            data.append([i])
        for idx, j in enumerate(self.power_curve["output_power"], start=0):
            data[idx].append(j)
        data.insert(0, ['Wind Speed', 'Output Power'])
        return data

    def compatibleGearboxes(self):
        gearboxes = self.gearbox_set.all()
        return gearboxes

    def compatibleGenerators(self):
        generators = self.generator_set.all()
        return generators

    def compatibleTowers(self):
        towers = self.tower_set.all()
        return towers

    def turbine_of_type(self):
        wf = Turbine.objects.filter(wec_typ__name__exact=self.name)
        return wf

    def swept_area(self):
        sw_ar = round(3.1416 * (self.rotor_diameter^2)/4, 2)
        return sw_ar

    def power_density(self):
        p_den = round(self.output_power/self.rotor_diameter, 2)
        return p_den

    class Meta:
        ordering = ('-updated',)
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('polls:wec_typ_detail', args=[self.id, self.slug])

