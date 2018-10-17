from phonenumber_field.modelfields import PhoneNumberField

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.contenttypes import fields

from turbine.models import Turbine
from wind_farms.models import Country

class Sector(models.Model):
    name = models.CharField(max_length=50, db_index=True)

    def __str__(self):
        return self.name

class Player(models.Model):

    name = models.CharField(max_length=75, db_index=True, verbose_name='Name', help_text="Enter the company's name")
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    adress = models.CharField(max_length=100, blank=True, help_text="Enter the postal address")
    postal_code = models.CharField(max_length=10, blank=True)
    city = models.CharField(max_length = 50, blank=True)
    country = models.ForeignKey(Country, blank=True, null=True)
    phone = PhoneNumberField(blank=True, help_text="Enter the phone number beginning with +")
    web = models.URLField(max_length=200, blank=True, help_text="Enter a vaild web address incl. http://")
    mail = models.EmailField(max_length=80, blank=True)

    customer_code = models.CharField(max_length=10, blank=True, help_text="Enter the customer code acc. to 'Projektübersicht'")
    sector = models.ManyToManyField('Sector', help_text="Choose at least one sector")
    comment = fields.GenericRelation('projects.Comment')

    available = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        ordering = ('name',)

    def relatedPersons(self):
        persons = self.person_set.all()
        return persons

    def relatedDevelopers(self):
        rel_developers = Turbine.objects.filter(developer=self, status__in=['in production', 'under construction', 'planned'])
        return rel_developers

    def relatedAsset_Management(self):
        rel_asset_management = Turbine.objects.filter(asset_management=self, status='in production')
        return rel_asset_management

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

    def relProjects(self):
        projects = self.project_customer.all()
        return projects

    def relContracts(self):
        contracts = self.turbine_contract_actor.all()
        return contracts

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('player:player_detail', args=[self.id, self.slug])

class Person(models.Model):

    name = models.CharField(max_length=50, db_index=True, verbose_name='Name', help_text="Surname and last name of the employee")
    company = models.ManyToManyField('Player', blank=True)
    function = models.CharField(max_length=50, blank=True, help_text="Role of the employee within its company")
    phone = PhoneNumberField(blank=True, help_text="Enter the phone number beginning with +")
    phone2 = PhoneNumberField(blank=True, help_text="Enter the phone number beginning with +")
    mail = models.EmailField(max_length=50, blank=True)
    comment = fields.GenericRelation('projects.Comment')
    available = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

    def related_projects(self):
        projects = self.customer_contact_projects.all()
        return projects

    def all_comments(self):
        comments = self.comment.exclude(text__in=['created employee', 'edited employee'])
        return comments

    def get_absolute_url(self):
        return reverse('player:person_detail', args=[self.id])