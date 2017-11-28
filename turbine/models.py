from django.db import models
from django.core.urlresolvers import reverse
from django.utils import timezone

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

class Turbine(models.Model):
    turbine_id = models.CharField(max_length=15, db_index=True)
    wind_farm = models.ForeignKey('wind_farms.WindFarm', blank=True, null=True)
    slug = models.SlugField(max_length=200, db_index=True)
    wec_manufacturer = models.ForeignKey('polls.Manufacturer', related_name='wec_manufacturers', verbose_name='Manufacturer')
    wec_typ = models.ForeignKey('polls.WEC_Typ', verbose_name='Model')
    hub_height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    commisioning = models.DateField(blank=True, null=True, verbose_name='Commisioning date')
    dismantling = models.DateField(blank=True, null=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    developer = models.ManyToManyField('player.Player', related_name='wec_developers', blank=True)
    com_operator = models.ManyToManyField('player.Player', related_name='wec_com_operators', verbose_name='Commercial operator', blank=True)
    tec_operator = models.ManyToManyField('player.Player', related_name='wec_tec_operators', verbose_name='Technicial operator',blank=True)
    owner = models.ForeignKey('player.Player', blank=True, null=True, related_name='wec_owners')
    service = models.ManyToManyField('player.Player', related_name='wec_service_providers', blank=True)
    offshore = models.CharField(max_length=50, choices=OFFSHORE, default='no')
    status = models.CharField(max_length=50, choices=STATUS, default='in production')
    repowered = models.BooleanField(default=False)
    follow_up_wec = models.ForeignKey('Turbine', verbose_name='Subsequent Turbine', blank=True, null=True)
    osm_id = models.CharField(max_length=25, blank=True, null=True)
    available = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        ordering = ('turbine_id',)
        index_together = (('id', 'slug'),)

    def developers(self):
        return self.developer.all()

    def com_operators(self):
        return self.com_operator.all()

    def tec_operators(self):
        return self.tec_operator.all()

    def service_providers(self):
        return self.service.all()

    def relContracts(self):
        contracts = self.contract_set.filter(available=True)
        return contracts

    def __str__(self):
        return self.turbine_id

    def get_absolute_url(self):
        return reverse('turbines:turbine_detail', args=[self.id, self.slug])

class Contract(models.Model):
    turbine = models.ForeignKey(Turbine, db_index=True)
    actor = models.ForeignKey('player.Player', related_name='turbine_contract_actor')
    contract_type = models.CharField(max_length=50, choices=CONTRACT_TYPE, default='service')
    start_date = models.DateField(blank=True, null=True, default=timezone.now)
    end_date = models.DateField(blank=True, null=True, default=timezone.now)
    available = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        ordering = ['start_date']