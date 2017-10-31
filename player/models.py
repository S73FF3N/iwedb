from django.db import models
from django.core.urlresolvers import reverse
from turbine.models import Turbine
from wind_farms.models import Country
from phonenumber_field.modelfields import PhoneNumberField

class Sector(models.Model):
    name = models.CharField(max_length=50, db_index=True)

    def __str__(self):
        return self.name

class Player(models.Model):

    name = models.CharField(max_length=50, db_index=True, verbose_name='Name')
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    adress = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    city = models.CharField(max_length = 50, blank=True, null=True)
    country = models.ForeignKey(Country, blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)
    web = models.URLField(max_length=50, blank=True, null=True)
    mail = models.EmailField(max_length=50, blank=True, null=True)
    sector = models.ManyToManyField('Sector')
    available = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def relatedDevelopers(self):
        rel_developers = Turbine.objects.filter(developer=self, status__in=['in production', 'under construction', 'planned'])
        return rel_developers

    def relatedCom_operators(self):
        rel_com_operators = Turbine.objects.filter(com_operator=self, status='in production')
        return rel_com_operators

    def relatedTec_operators(self):
        rel_tec_operators = Turbine.objects.filter(tec_operator=self, status='in production')
        return rel_tec_operators

    def relatedOwners(self):
        rel_owners = Turbine.objects.filter(owner=self, status__in=['in production', 'under construction', 'planned'])
        return rel_owners

    def relatedService(self):
        rel_service = Turbine.objects.filter(service=self, status='in production')
        return rel_service

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('player:player_detail', args=[self.id, self.slug])