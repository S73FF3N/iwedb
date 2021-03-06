from phonenumber_field.modelfields import PhoneNumberField

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields
from django.utils.translation import ugettext_lazy as _

from turbine.models import Turbine, Contract
from projects.models import Project
from wind_farms.models import Country

GENDER = (
    ('male', _('male')),
    ('female', _('female')),
    ('divers', _('divers')),)

class Sector(models.Model):
    name = models.CharField(max_length=50, db_index=True)

    def __str__(self):
        return self.name

class File(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    file = models.FileField(upload_to='actor_files/%Y/%m/%d/', verbose_name=_("File"))
    available = models.BooleanField(default=True)

    limit = models.Q(app_label = 'player', model='player')
    content_type = models.ForeignKey(ContentType, limit_choices_to=limit, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = fields.GenericForeignKey('content_type', 'object_id')

    created = models.DateField(auto_now_add=True, db_index=True)
    created_by = models.ForeignKey('auth.User')

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.name


class Player(models.Model):

    name = models.CharField(max_length=75, db_index=True, verbose_name='Name', help_text=_("Enter the company's name"))
    slug = models.SlugField(max_length=200, db_index=True, unique=True)

    adress = models.CharField(max_length=100, blank=True, help_text=_("Enter the postal address"), verbose_name=_("Address"))
    postal_code = models.CharField(max_length=10, blank=True, verbose_name=_("Postal Code"))
    city = models.CharField(max_length = 50, blank=True, verbose_name=_("City"))
    country = models.ForeignKey(Country, verbose_name=_("Country"))
    phone = PhoneNumberField(blank=True, help_text=_("Enter the phone number beginning with +"), verbose_name=_("Phone"))
    web = models.URLField(max_length=200, blank=True, help_text=_("Enter a vaild web address incl. http://"))
    mail = models.EmailField(max_length=80, blank=True)

    customer_code = models.CharField(max_length=10, blank=True, null=True, help_text=_("Enter the customer code acc. to 'Projektübersicht'"), verbose_name=_("Customer Code"))
    sector = models.ManyToManyField('Sector', help_text=_("Choose at least one sector"), verbose_name=_("Sector"))
    head_organisation = models.ForeignKey('Player', blank=True, null=True, verbose_name=_("Head Organisation"))
    comment = fields.GenericRelation('projects.Comment', verbose_name=_("Comment"))
    file = fields.GenericRelation('File', verbose_name=_("File"))

    available = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        ordering = ('name',)
        permissions = (("comment_on_person", "Can comment on persons"),)

    def headed_organisations(self):
        organisations = Player.objects.filter(head_organisation=self, available=True)
        return organisations

    def relatedPersons(self):
        persons = self.person_set.filter(available=True)
        return persons

    def developed_turbines(self):
        rel_turbines = Turbine.objects.filter(developer=self, status__in=['in production', 'under construction', 'planned'])
        return rel_turbines

    def asset_managed_turbines(self):
        rel_turbines = Turbine.objects.filter(asset_management=self, status='in production')
        return rel_turbines

    def com_operated_turbines(self):
        rel_turbines = Turbine.objects.filter(com_operator=self, status='in production')
        return rel_turbines

    def tec_operated_turbines(self):
        rel_turbines = Turbine.objects.filter(tec_operator=self, status='in production')
        return rel_turbines

    def owned_turbines(self):
        rel_turbines = Turbine.objects.filter(owner=self, status__in=['in production', 'under construction', 'planned'])
        return rel_turbines

    def serviced_turbines(self):
        rel_turbines = Turbine.objects.filter(service=self, status='in production')
        return rel_turbines

    def relProjects(self):
        projects = self.project_customer.all()
        return projects

    def relPoolProjects(self):
        pools = self.pool_customer.all()
        return pools

    def relContracts(self):
        contracts = self.turbine_contract_actor.all()
        return contracts

    def related_indirect_contracts(self):
        asset_managed_turbines = self.asset_managed_turbines()
        com_operated_turbines = self.com_operated_turbines()
        tec_operated_turbines = self.tec_operated_turbines()
        owned_turbines = self.owned_turbines()

        related_turbines = asset_managed_turbines | com_operated_turbines | tec_operated_turbines | owned_turbines

        related_turbine_ids = related_turbines.all().prefetch_related('contracted_turbines').values_list('id', flat=True)
        related_contract_ids = Contract.objects.filter(turbines__in=related_turbine_ids).values_list('id', flat=True).distinct()

        direct_related_contract_ids = self.relContracts().values_list('id', flat=True)
        indirect_related_contract_ids = list(set(related_contract_ids) - set(direct_related_contract_ids))

        indirect_related_contracts = Contract.objects.filter(id__in=indirect_related_contract_ids)

        return indirect_related_contracts

    def related_indirect_projects(self):
        asset_managed_turbines = self.asset_managed_turbines()
        com_operated_turbines = self.com_operated_turbines()
        tec_operated_turbines = self.tec_operated_turbines()
        owned_turbines = self.owned_turbines()

        related_turbines = asset_managed_turbines | com_operated_turbines | tec_operated_turbines | owned_turbines

        related_turbine_ids = related_turbines.all().prefetch_related('contracted_turbines').values_list('id', flat=True)
        related_project_ids = Project.objects.filter(turbines__in=related_turbine_ids).values_list('id', flat=True).distinct()

        direct_related_project_ids = self.relProjects().values_list('id', flat=True)
        indirect_related_project_ids = list(set(related_project_ids) - set(direct_related_project_ids))

        indirect_related_projects = Project.objects.filter(id__in=indirect_related_project_ids)

        return indirect_related_projects

    def all_comments(self):
        comments = self.comment.exclude(text__in=['created actor', 'edited actor', "Marktteilnehmer angelegt", "Marktteilnehmer editiert"])
        return comments

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('player:player_detail', args=[self.id, self.slug])

class MailingList(models.Model):
    name = models.CharField(max_length=40, db_index=True)
    #name_ger = models.CharField(max_length=40, db_index=True)
    description = models.TextField()
    #description_ger = models.TextField()

    def __str__(self):
        return self.name

class Person(models.Model):

    gender = models.CharField(max_length=15, choices=GENDER, default="divers", db_index=True, help_text=_("Gender of the employee"))
    first_name = models.CharField(max_length=50, db_index=True, verbose_name='First Name', help_text=_("First name of the employee"))
    name = models.CharField(max_length=50, db_index=True, verbose_name='Last Name', help_text=_("Last name of the employee"))
    company = models.ManyToManyField('Player', verbose_name=_("Company"))
    function = models.CharField(max_length=50, blank=True, help_text=_("Role of the employee within its company"), verbose_name=_("Function"))
    phone = PhoneNumberField(blank=True, help_text=_("Enter the phone number beginning with +"), verbose_name=_("Phone"))
    phone2 = PhoneNumberField(blank=True, help_text=_("Enter the phone number beginning with +"), verbose_name=_("Phone"))
    mail = models.EmailField(max_length=50, blank=True)
    postal_communication = models.BooleanField(default=False, verbose_name=_("Postal communication"), help_text=_("For marketing communication: Check if the contact preferes postal over digital communication."))

    adress = models.CharField(max_length=100, blank=True, help_text=_("Enter the postal address"), verbose_name=_("Street and house number"))
    postal_code = models.CharField(max_length=10, blank=True, verbose_name=_("Postal Code"))
    city = models.CharField(max_length = 50, blank=True, verbose_name=_("City"))
    country = models.ForeignKey(Country, verbose_name=_("Country"))

    mailing_list = models.ManyToManyField('MailingList', blank=True, verbose_name=_("Mailing List"))

    comment = fields.GenericRelation('projects.Comment', verbose_name=_("Comment"))

    available = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

    def _company_name(self):
        companies = self.company.all()
        company_name = [x for x in companies]
        return ", ".join([str(x) for x in company_name])
    company_name = property(_company_name)

    def _mailing_list_name(self):
        mailing_lists = self.mailing_list.all()
        mailing_list_name = [x for x in mailing_lists]
        return ", ".join([str(x) for x in mailing_list_name])
    mailing_list_name = property(_mailing_list_name)

    def related_projects(self):
        projects = self.customer_contact_projects.all()
        return projects

    def all_comments(self):
        comments = self.comment.exclude(text__in=[_('created employee'), _('edited employee')])
        return comments

    def get_absolute_url(self):
        return reverse('player:person_detail', args=[self.id])