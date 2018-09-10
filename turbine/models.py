from django.db import models
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.contrib.contenttypes import fields
from django.db.models import Min

from datetime import datetime

from projects.models import DWT

STATUS = (
    ('in production', 'in production'),
    ('under construction', 'under construction'),
    ('planned', 'planned'),
    ('dismantled', 'dismantled'),)


OFFSHORE = (
    ('yes', 'yes'),
    ('no', 'no'),)

CONTRACT_TYPE = (
    ('commercial management', 'Commercial management'),
    ('technical operations', 'Technical operations'),
    ('service', 'Service'),)

LOCATION = (
    ('External Storage', 'External Storage'),
    ('Engineering', 'Engineering'),
    ('Vehicle', 'Vehicle'),
    ('North-East', 'North-East'),
    ('North-West', 'North-West'),
    ('Head Quarter', 'Head Quarter'),
    ('South-East', 'South-East'),
    ('South-West', 'South-West'),
    ('Transfer Storage', 'Transfer Storage'),)

class Turbine(models.Model):
    turbine_id = models.CharField(max_length=25, db_index=True)
    wind_farm = models.ForeignKey('wind_farms.WindFarm', blank=True, null=True, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    wec_typ = models.ForeignKey('polls.WEC_Typ', verbose_name='Model', db_index=True)
    hub_height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    commisioning = models.DateField(blank=True, null=True, verbose_name='Commisioning date')
    dismantling = models.DateField(blank=True, null=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    developer = models.ManyToManyField('player.Player', related_name='wec_developers', blank=True)
    asset_management = models.ManyToManyField('player.Player', related_name='wec_asset_management', verbose_name='Asset Management', blank=True)
    com_operator = models.ManyToManyField('player.Player', related_name='wec_com_operators', verbose_name='Commercial operator', blank=True)
    tec_operator = models.ManyToManyField('player.Player', related_name='wec_tec_operators', verbose_name='Technicial operator',blank=True)
    owner = models.ForeignKey('player.Player', blank=True, null=True, related_name='wec_owners')
    service = models.ManyToManyField('player.Player', related_name='wec_service_providers', blank=True)
    offshore = models.CharField(max_length=50, choices=OFFSHORE, default='no')
    status = models.CharField(max_length=50, choices=STATUS, default='in production')
    repowered = models.BooleanField(default=False)
    follow_up_wec = models.ForeignKey('Turbine', verbose_name='Subsequent Turbine', blank=True, null=True)
    osm_id = models.CharField(max_length=25, blank=True, null=True)
    comment = fields.GenericRelation('projects.Comment')
    available = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        ordering = ('turbine_id',)
        index_together = (('id', 'slug'),)

    def developers(self):
        return self.developer.all()

    def asset_managements(self):
        return self.asset_management.all()

    def com_operators(self):
        return self.com_operator.all()

    def tec_operators(self):
        return self.tec_operator.all()

    def service_providers(self):
        return self.service.all()

    def relContracts(self):
        contracts = self.contracted_turbines.all()
        return contracts

    def relProjects(self):
        projects = self.project_turbines.all()
        return projects

    def yearpublished(self):
        return self.commisioning.strftime('%Y')

    def __str__(self):
        return self.turbine_id

    def get_absolute_url(self):
        return reverse('turbines:turbine_detail', args=[self.id, self.slug])

class Contract(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    file = models.FileField(upload_to='contract_files/%Y/%m/%d/', null=True, blank=True)
    turbines = models.ManyToManyField(Turbine, related_name='contracted_turbines', verbose_name='Turbines', db_index=True)
    actor = models.ForeignKey('player.Player', related_name='turbine_contract_actor')
    start_date = models.DateField(blank=True, null=True, default=timezone.now)
    end_date = models.DateField(blank=True, null=True, default=timezone.now)

    contact_customer = models.ManyToManyField('player.Person', blank=True, related_name='customer_contact_contracts', verbose_name='Customer Contact')
    contact_tec = models.ManyToManyField('player.Person', blank=True, related_name='contact_tec_contracts', verbose_name='Contact Technical Operations')
    contact_com = models.ManyToManyField('player.Person', blank=True, related_name='contact_com_contracts', verbose_name='Contact Commercial Operations')

    average_remuneration = models.DecimalField(max_digits=8, decimal_places=2, default=35000)
    farm_availability = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    wtg_availability = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)

    remote_control = models.BooleanField(default=False)
    scheduled_maintenance = models.BooleanField(default=False)
    unscheduled_maintenance_personnel = models.BooleanField(default=False)
    unscheduled_maintenance_material = models.BooleanField(default=False)
    main_components = models.BooleanField(default=False)
    rotor_excluded = models.BooleanField(default=False)
    external_damages = models.BooleanField(default=False)

    comment = fields.GenericRelation('projects.Comment')

    active = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        ordering = ['start_date']

    def get_absolute_url(self):
        return reverse('turbines:contract_detail', args=[self.id])

    def contracted_windfarm(self):
        windfarms = {t.wind_farm.name : t.wind_farm.get_absolute_url() for t in self.turbines.all()}
        return windfarms

    def contracted_windfarm_name(self):
        windfarms = self.turbines.all().order_by().values_list("wind_farm__name", flat=True).distinct()
        if len(windfarms) == 1:
            return windfarms[0]
        else:
            return ", ".join([str(x) for x in windfarms])

    def contracted_wec_types(self):
        oem_name = self.turbines.all().order_by().values_list("wec_typ__manufacturer__name", flat=True).distinct()
        wec_typ_name = self.turbines.all().order_by().values_list("wec_typ__name", flat=True).distinct()
        models_name = []
        for i in range(len(oem_name)):
            models_name.append(" ".join([oem_name[i], wec_typ_name[i]]))
        models_link = [t.wec_typ.get_absolute_url() for t in self.turbines.all()]
        models_link = list(set(models_link))
        models = dict(zip(models_name, models_link))
        return models

    def contracted_wec_types_name(self):
        models = self.turbines.all().order_by().values_list("wec_typ__name", flat=True).distinct()
        if len(models) == 1:
            return models[0]
        else:
            return ", ".join([str(x) for x in models])

    def contracted_oem_name(self):
        oems = self.turbines.all().order_by().values_list("wec_typ__manufacturer__name", flat=True).distinct()
        if len(oems) == 1:
            return oems[0]
        else:
            return ", ".join([str(x) for x in oems])

    def amount_turbines(self):
        contracted_turbines = self.turbines.all().count()
        return contracted_turbines

    def mw(self):
        mw = sum(self.turbines.all().order_by().values_list('wec_typ__output_power', flat=True))*0.001
        return round(mw, 2)

    def turbine_age(self):
        try:
            first_commisioning = self.turbines.all().aggregate(first=Min('commisioning'))['first']
            try:
                start = self.start_operation.year
            except:
                start = datetime.now().year
            age = start - first_commisioning.year
            if age < 0:
                age = 0
        except:
            age = 'not defined'
        return age

    def __str__(self):
        return self.name

class ServiceLocation(models.Model):
    name = models.CharField(max_length=100, db_index=True, default="Osnabrück")
    postal_code = models.CharField(max_length=20, default="49082")
    dwt = models.CharField(max_length=30, choices=DWT, default='DWTX')
    location_type = models.CharField(max_length=50, choices=LOCATION, default='Vehicle')

    latitude = models.FloatField()
    longitude = models.FloatField()

    active = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.name