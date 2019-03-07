from django.db import models
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.contrib.contenttypes import fields
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy

from datetime import datetime, date

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

YEAR_CHOICES = [(y,y) for y in range(1990, datetime.today().year+6)]
MONTH_CHOICES = [(m,m) for m in range(1,13)]
DAY_CHOICES = [(d,d) for d in range(1,32)]

class Exclusion(models.Model):
    name = models.CharField(max_length=50, db_index=True)

    def __str__(self):
        return self.name

class Turbine(models.Model):
    turbine_id = models.CharField(max_length=25, db_index=True, help_text='If Turbine ID is unknown use this scheme: <Windfarm name>01. NEG turbines should be labeled by the Vestas abbreviation "V".')
    wind_farm = models.ForeignKey('wind_farms.WindFarm', blank=True, null=True, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    wec_typ = models.ForeignKey('polls.WEC_Typ', verbose_name='Model', db_index=True, help_text="Enter the turbine type (e.g. V90) not the manufacturer (e.g. Vestas)!")
    hub_height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text='Hub height in meters')
    commisioning_year = models.IntegerField(choices=YEAR_CHOICES, blank=True, null=True)
    commisioning_month = models.IntegerField(choices=MONTH_CHOICES, blank=True, null=True)
    commisioning_day = models.IntegerField(choices=DAY_CHOICES, blank=True, null=True)
    dismantling_year = models.IntegerField(choices=YEAR_CHOICES, blank=True, null=True)
    dismantling_month = models.IntegerField(choices=MONTH_CHOICES, blank=True, null=True)
    dismantling_day = models.IntegerField(choices=DAY_CHOICES, blank=True, null=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    developer = models.ManyToManyField('player.Player', related_name='wec_developers', blank=True, help_text='Specify the company which developed the turbine')
    asset_management = models.ManyToManyField('player.Player', related_name='wec_asset_management', verbose_name='Asset Management', blank=True, help_text="Specify the company which manages the turbine's asset")
    com_operator = models.ManyToManyField('player.Player', related_name='wec_com_operators', verbose_name='Commercial operator', blank=True, help_text='Specify the company which commercially manages the turbine')
    tec_operator = models.ManyToManyField('player.Player', related_name='wec_tec_operators', verbose_name='Technicial operator',blank=True, help_text='Specify the company which technically operates the turbine')
    owner = models.ForeignKey('player.Player', blank=True, null=True, related_name='wec_owners', help_text='Specify the company which owns the turbine')
    service = models.ManyToManyField('player.Player', related_name='wec_service_providers', blank=True, help_text='Specify the company which currently services the turbine')
    offshore = models.CharField(max_length=50, choices=OFFSHORE, default='no', help_text='Is this turbine built offshore')
    status = models.CharField(max_length=50, choices=STATUS, default='in production')
    repowered = models.BooleanField(default=False, help_text='If the turbine has been dismantled, has it been repowered afterwards?')
    follow_up_wec = models.ForeignKey('Turbine', verbose_name='Subsequent Turbine', blank=True, null=True, help_text='If it has been repowered, by which turbine?')
    osm_id = models.CharField(max_length=25, blank=True, help_text='Openstreetmap ID')
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

    def _wec_typ_name(self):
        wec_typ = self.wec_typ.__str__()
        return wec_typ
    wec_typ_name = property(_wec_typ_name)

    def commisioning_date(self):
        if self.commisioning_year and self.commisioning_month and self.commisioning_day:
            return {'date': date(self.commisioning_year, self.commisioning_month, self.commisioning_day), 'exact': 2}
        elif self.commisioning_year and self.commisioning_month:
            return {'date': date(self.commisioning_year, self.commisioning_month, 1), 'exact': 1}
        elif self.commisioning_year:
            return {'date': date(self.commisioning_year, 1, 1), 'exact': 0}
        else:
            return None

    def dismantling_date(self):
        if self.dismantling_year and self.dismantling_month and self.dismantling_day:
            return {'date': date(self.dismantling_year, self.dismantling_month, self.dismantling_day), 'exact': 2}
        elif self.dismantling_year and self.dismantling_month:
            return {'date': date(self.dismantling_year, self.dismantling_month, 1), 'exact': 1}
        elif self.dismantling_year:
            return {'date': date(self.dismantling_year, 1, 1), 'exact': 0}
        else:
            return None

    def __str__(self):
        return self.turbine_id

    def get_absolute_url(self):
        return reverse('turbines:turbine_detail', args=[self.id, self.slug])

class Contract(models.Model):
    name = models.CharField(max_length=100, db_index=True, help_text='Enter a name for the contract acc. to the scheme of the placeholder')
    file = models.FileField(upload_to='contract_files/%Y/%m/%d/', null=True, blank=True, help_text='Attach the pdf file of the contract')
    turbines = models.ManyToManyField(Turbine, related_name='contracted_turbines', verbose_name='Turbines', db_index=True, help_text='Add all turbines included in this contract')
    actor = models.ForeignKey('player.Player', related_name='turbine_contract_actor', verbose_name="Contractual Partner", help_text='Enter the contractual partner')
    dwt = models.CharField(max_length=30, choices=DWT, default='DWTX', verbose_name="DWT Unit")
    start_date = models.DateField(blank=True, null=True, default=timezone.now, help_text='Enter the effective commencement date of this contract')
    end_date = models.DateField(blank=True, null=True, default=timezone.now, help_text='Enter the effective end date of this contract')

    contact_customer = models.ManyToManyField('player.Person', blank=True, related_name='customer_contact_contracts', verbose_name='Customer Contact', help_text='Enter the contact person of the customer')
    contact_tec = models.ManyToManyField('player.Person', blank=True, related_name='contact_tec_contracts', verbose_name='Contact Technical Operations', help_text='Enter the contact person of the technical operator')
    contact_com = models.ManyToManyField('player.Person', blank=True, related_name='contact_com_contracts', verbose_name='Contact Commercial Operations', help_text='Enter the contact person of the commercial operator')

    average_remuneration = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, help_text='Enter the average remuneration per year and WTG of this contract')
    farm_availability = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True, help_text='Availability Guarantee for the wind farm in %')
    wtg_availability = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True, help_text='Availability Guarantee for single WTG in %')

    remote_control = models.BooleanField(default=False, help_text='Is remote control included?')
    scheduled_maintenance = models.BooleanField(default=False, help_text='Is scheduled maintenance included?')
    additional_maintenance = models.BooleanField(default=False, help_text='Are additional scheduled maintenances (e.g. TypeIV) included?')
    unscheduled_maintenance_personnel = models.BooleanField(default=False, help_text='Is personnel for unscheduled maintenance included?')
    unscheduled_maintenance_material = models.BooleanField(default=False, help_text='Are materials for unscheduled maintenance included?')
    main_components = models.BooleanField(default=False, help_text='Are main components included?')

    exclusions = models.ManyToManyField('Exclusion', help_text='Which components are exluded from the scope?', blank=True)

    external_damages = models.BooleanField(default=False, help_text='Is an insurance for external damages included?')
    pressure_vessels = models.BooleanField(default=False, help_text='Is the replacement of pressure vessels included?')
    overhaul_working_equipment = models.BooleanField(default=False, help_text='Is the general overhaul of working equipment (winch, on-board crane, etc.) included?')
    cms = models.BooleanField(default=False, help_text='Is a permanent condition monitoring included?')

    rotor_blade_inspection = models.BooleanField(default=False, help_text='Are rotor blade inspections included?')
    videoendoscopic_inspection_gearbox = models.BooleanField(default=False, help_text='Are videoendoscopic inspections of the gearbox included?')
    periodic_inspection_wtg = models.BooleanField(default=False, help_text='Are periodic inspections of the WTG (WKP) included?')

    service_lift_maintenance = models.BooleanField(default=False, help_text='Is service lift maintenance included?')
    safety_inspection = models.BooleanField(default=False, help_text='Is the inspection of safety equipment (PSE, fire extinguisher, etc.) included?')
    safety_repairs = models.BooleanField(default=False, help_text='Is the repair of safety equipment (PSE, fire extinguisher, etc.) included?')
    safety_exchange = models.BooleanField(default=False, help_text='Is the repair of safety equipment (PSE, fire extinguisher, etc.) included?')

    certified_body_inspection_service_lift = models.BooleanField(default=False, help_text='Is the inspection of the service lift by a certified body (ZÜS) included?')
    electrical_inspection = models.BooleanField(default=False, help_text='Are the electrical inspection (DGUV V3) included?')

    comment = fields.GenericRelation('projects.Comment')

    active = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        ordering = ['start_date']
        permissions = (("can_comment_contracts", "Can write comments on contracts."),
                        ("can_view_contract_pdf", "Can view contract pdf."),
                        ("can_terminate_contract", "Can terminate contract"),
                        ("can_create_custom_export_of_contracts", "Can create a custom export of contracts"),)

    def get_absolute_url(self):
        return reverse('turbines:contract_detail', args=[self.id])

    def _contracted_windfarm(self):
        turbines = self.turbines.all()
        windfarms = {t.wind_farm.name : t.wind_farm.get_absolute_url() for t in turbines}
        return windfarms
    contracted_windfarm = property(_contracted_windfarm)

    def _contracted_country(self):
        turbines = self.turbines.all()
        country = list(set([str(t.wind_farm.country.name) for t in turbines]))
        if len(country) == 1:
            return country[0]
        else:
            return ", ".join([str(x) for x in country])
    contracted_country = property(_contracted_country)

    def _contracted_windfarm_name(self):
        turbines = self.turbines.all()
        windfarms = list(set([str(x.wind_farm.name) for x in turbines]))
        if len(windfarms) == 1:
            return windfarms[0]
        else:
            return ", ".join([str(x) for x in windfarms])
    contracted_windfarm_name = property(_contracted_windfarm_name)

    def _contracted_wec_types(self):
        oem_name = list(set([str(x.wec_typ.manufacturer.name) for x in self.turbines.all()]))
        wec_typ_name = list(set([str(x.wec_typ.name) for x in self.turbines.all()]))
        models_name = []
        for i in range(len(oem_name)):
            models_name.append(" ".join([oem_name[i], wec_typ_name[i]]))
        turbines = self.turbines.all()
        models_link = [t.wec_typ.get_absolute_url() for t in turbines]
        models_link = list(set(models_link))
        models = dict(zip(models_name, models_link))
        return models
    contracted_wec_types = property(_contracted_wec_types)

    def _contracted_wec_types_name(self):
        models = list(set([str(x.wec_typ.name) for x in self.turbines.all()]))
        if len(models) == 1:
            return models[0]
        else:
            return ", ".join([str(x) for x in models])
    contracted_wec_types_name = property(_contracted_wec_types_name)

    def _contracted_oem_name(self):
        oems = list(set([str(x.wec_typ.manufacturer.name) for x in self.turbines.all()]))
        if len(oems) == 1:
            return oems[0]
        else:
            return ", ".join([str(x) for x in oems])
    contracted_oem_name = property(_contracted_oem_name)

    def _amount_turbines(self):
        contracted_turbines = self.turbines.count()
        return contracted_turbines
    amount_turbines = property(_amount_turbines)

    def _mw(self):
        mw = sum(self.turbines.order_by().values_list('wec_typ__output_power', flat=True))*0.001
        return round(mw, 2)
    mw = property(_mw)

    def _turbine_age(self):
        try:
            first_commisioning = self.first_commisioning
            try:
                start = self.start_operation.year
            except:
                start = datetime.now().year
            age = start - first_commisioning
            if age < 0:
                age = 0
        except:
            age = 'not defined'
        return age
    turbine_age = property(_turbine_age)

    def _contract_coordinates(self):
        longitude = self.turbines.all()[0].wind_farm.longitude
        latitude = self.turbines.all()[0].wind_farm.latitude
        return {'latitude': latitude, 'longitude': longitude}
    contract_coordinates = property(_contract_coordinates)

    def _contract_scope(self):
        if self.main_components == True:
            scope = "Full maintenance with MC"
        elif self.unscheduled_maintenance_material == True and self.main_components != True:
            scope = "Full maintenance without MC"
        elif self.scheduled_maintenance == True and self.main_components != True and self.unscheduled_maintenance_material != True and self.unscheduled_maintenance_personnel != True:
            scope = "Basic"
        elif self.unscheduled_maintenance_personnel == True and self.main_components != True and self.unscheduled_maintenance_material != True:
            scope = "Basic +"
        elif self.remote_control == True and self.main_components != True and self.unscheduled_maintenance_material != True and self.unscheduled_maintenance_personnel != True and self.scheduled_maintenance != True:
            scope = "Remote Control"
        else:
            scope = "Other"
        return scope
    contract_scope = property(_contract_scope)

    def __str__(self):
        return self.name

class ServiceLocation(models.Model):
    name = models.CharField(max_length=100, db_index=True, default="Osnabrück")
    postal_code = models.CharField(max_length=20, default="49082")
    dwt = models.CharField(max_length=30, choices=DWT, default='DWTX')
    location_type = models.CharField(max_length=50, choices=LOCATION, default='Vehicle')
    supported_technology = models.ManyToManyField('polls.Manufacturer')

    latitude = models.FloatField()
    longitude = models.FloatField()

    active = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.name