from django.db import models
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.contrib.contenttypes import fields
from django.utils.translation import ugettext_lazy as _

from datetime import datetime, date

from projects.models import DWT
import polls.models

STATUS = (
    ('in production', _('in production')),
    ('under construction', _('under construction')),
    ('planned', _('planned')),
    ('dismantled', _('dismantled')),)

OFFSHORE = (
    ('yes', _('yes')),
    ('no', _('no')),)

AVAILABILITY = (
    ('time based', _('time based')),
    ('energy based', _('energy based')),)

LOCATION = (
    ('External Storage', _('External Storage')),
    ('Engineering', _('Engineering')),
    ('Vehicle', _('Vehicle')),
    ('North-East', _('North-East')),
    ('North-West', _('North-West')),
    ('Head Quarter', _('Head Quarter')),
    ('South-East', _('South-East')),
    ('South-West', _('South-West')),
    ('South', _('South')),
    ('Middle', _('Middle')),
    ('Transfer Storage', _('Transfer Storage')),)

TERMINATION_REASON = (
    ('Closure of WTG / business', _('Closure of WTG / business')),
    ('Alteration of Contract', _('Alteration of Contract')),
    ('Competition', _('Competition')),
    ('Change of Ownership', _('Change of Ownership')),
    ('Breach of Agreement', _('Breach of Agreement')),
    ('Bankruptcy', _('Bankruptcy')),
    ('Corporate Structure', _('Corporate Structure')),
    )

YEAR_CHOICES = [(y,y) for y in range(1990, datetime.today().year+6)]
MONTH_CHOICES = [(m,m) for m in range(1,13)]
DAY_CHOICES = [(d,d) for d in range(1,32)]

class Exclusion(models.Model):
    name = models.CharField(max_length=50, db_index=True)

    def __str__(self):
        return self.name

class Turbine(models.Model):
    turbine_id = models.CharField(max_length=25, db_index=True, help_text=_('If Turbine ID is unknown use this scheme: WindfarmName01. NEG turbines should be labeled by the Vestas abbreviation "V".'), verbose_name=_("Turbine ID"))
    wind_farm = models.ForeignKey('wind_farms.WindFarm', db_index=True, verbose_name=_("Wind Farm"))
    slug = models.SlugField(max_length=200, db_index=True)
    wec_typ = models.ForeignKey('polls.WEC_Typ', verbose_name=_('Model'), db_index=True, help_text=_("Enter the turbine type (e.g. V90) not the manufacturer (e.g. Vestas)!"))
    hub_height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text=_('Hub height in meters'), verbose_name=_("Hub Height"))
    commisioning_year = models.IntegerField(choices=YEAR_CHOICES, blank=True, null=True, verbose_name=_("Commisioning Year"))
    commisioning_month = models.IntegerField(choices=MONTH_CHOICES, blank=True, null=True, verbose_name=_("Commisioning Month"))
    commisioning_day = models.IntegerField(choices=DAY_CHOICES, blank=True, null=True, verbose_name=_("Commisioning Day"))
    dismantling_year = models.IntegerField(choices=YEAR_CHOICES, blank=True, null=True, verbose_name=_("Dismantling Year"))
    dismantling_month = models.IntegerField(choices=MONTH_CHOICES, blank=True, null=True, verbose_name=_("Dismantling Month"))
    dismantling_day = models.IntegerField(choices=DAY_CHOICES, blank=True, null=True, verbose_name=_("Dismantling Day"))
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    developer = models.ManyToManyField('player.Player', related_name='wec_developers', blank=True, help_text=_('Specify the company which developed the turbine'), verbose_name=_("Developer"))
    asset_management = models.ManyToManyField('player.Player', related_name='wec_asset_management', blank=True, help_text=_("Specify the company which manages the turbine's asset"))
    com_operator = models.ManyToManyField('player.Player', related_name='wec_com_operators', verbose_name=_('Commercial operator'), blank=True, help_text=_('Specify the company which commercially manages the turbine'))
    tec_operator = models.ManyToManyField('player.Player', related_name='wec_tec_operators', verbose_name=_('Technicial operator'),blank=True, help_text=_('Specify the company which technically operates the turbine'))
    owner = models.ForeignKey('player.Player', blank=True, null=True, related_name='wec_owners', help_text=_('Specify the company which owns the turbine'), verbose_name=_("Owner"))
    service = models.ManyToManyField('player.Player', related_name='wec_service_providers', blank=True, help_text=_('Specify the company which currently services the turbine'), verbose_name=_("Service Company"))
    offshore = models.CharField(max_length=50, choices=OFFSHORE, default='no', help_text=_('Is this turbine built offshore'))
    status = models.CharField(max_length=50, choices=STATUS, default='in production')
    repowered = models.BooleanField(default=False, help_text=_('If the turbine has been dismantled, has it been repowered afterwards?'), verbose_name=_("Repowered"))
    follow_up_wec = models.ForeignKey('Turbine', verbose_name='Subsequent Turbine', blank=True, null=True, help_text=_('If it has been repowered, by which turbine?'))
    osm_id = models.CharField(max_length=25, blank=True, help_text=_('Openstreetmap ID'), verbose_name="Openstreetmap")
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

    def relEvents(self):
        events = self.event_turbines.all()
        return events

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
    name = models.CharField(max_length=100, db_index=True, help_text=_('Enter a name for the contract acc. to the scheme of the placeholder'))
    file = models.FileField(upload_to='contract_files/%Y/%m/%d/', null=True, blank=True, help_text=_('Attach the pdf file of the contract'), verbose_name=_("File"))
    turbines = models.ManyToManyField(Turbine, related_name='contracted_turbines', verbose_name=_('Turbines'), db_index=True, help_text=_('Add all turbines included in this contract'))
    actor = models.ForeignKey('player.Player', related_name='turbine_contract_actor', verbose_name=_("Contractual Partner"), help_text=_('Enter the contractual partner'))
    dwt = models.CharField(max_length=30, choices=DWT, default='DWTX', verbose_name=_("DWT Unit"))
    start_date = models.DateField(blank=True, null=True, default=timezone.now, help_text=_('Enter the effective commencement date of this contract'), verbose_name=_("Start Date"))
    end_date = models.DateField(blank=True, null=True, default=timezone.now, help_text=_('Enter the effective end date of this contract'), verbose_name=_("End Date"))

    termination_date = models.DateField(blank=True, null=True, help_text=_('Enter the date when the contract was terminated by the customer.'), verbose_name=_("Termination Date"))
    termination_reason = models.CharField(max_length=30, choices=TERMINATION_REASON, blank=True, null=True, help_text=_("Which reason lead to the termination of the contract?"), verbose_name=_("Termination Reason"))

    # not used
    contact_customer = models.ManyToManyField('player.Person', blank=True, related_name='customer_contact_contracts', verbose_name=_('Customer Contact'), help_text=_('Enter the contact person of the customer'))
    contact_tec = models.ManyToManyField('player.Person', blank=True, related_name='contact_tec_contracts', verbose_name=_('Contact Technical Operations'), help_text=_('Enter the contact person of the technical operator'))
    contact_com = models.ManyToManyField('player.Person', blank=True, related_name='contact_com_contracts', verbose_name=_('Contact Commercial Operations'), help_text=_('Enter the contact person of the commercial operator'))
    # end not used

    dwt_responsible = models.ForeignKey('auth.User', blank=True, null=True, help_text=_("Who is the responsible Customer Relation Manager?"), verbose_name=_("DWT Responsible"))

    average_remuneration = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, help_text=_('Enter the average remuneration per year and WTG of this contract'), verbose_name=_("Average Remuneration"))
    farm_availability = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True, help_text=_('Availability Guarantee for the wind farm in %'), verbose_name=_("Farm Availability"))
    wtg_availability = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True, help_text=_('Availability Guarantee for single WTG in %'), verbose_name=_("WTG Availability"))
    availability_type = models.CharField(max_length=20, choices=AVAILABILITY, blank=True, null=True, verbose_name=_("Availabiltiy Type"))

    remote_control = models.BooleanField(default=False, help_text=_('Is remote control included?'), verbose_name=_("Remote Control"))
    scheduled_maintenance = models.BooleanField(default=False, help_text=_('Is scheduled maintenance included?'), verbose_name=_("Scheduled Maintenance"))
    additional_maintenance = models.BooleanField(default=False, help_text=_('Are additional scheduled maintenances (e.g. TypeIV) included?'), verbose_name=_("Additional Maintenance"))
    unscheduled_maintenance_personnel = models.BooleanField(default=False, help_text=_('Is personnel for unscheduled maintenance included?'), verbose_name=_("Unscheduled Maintenance Personnel"))
    unscheduled_maintenance_material = models.BooleanField(default=False, help_text=_('Are materials for unscheduled maintenance included?'), verbose_name=_("Unscheduled Maintenance Material"))
    main_components = models.BooleanField(default=False, help_text=_('Are main components included?'), verbose_name=_("Main Components"))

    exclusions = models.ManyToManyField('Exclusion', help_text=_('Which components are exluded from the scope?'), verbose_name=_("Exclusions"), blank=True)

    technical_operation = models.BooleanField(default=False, help_text=_('Is techncial operation included?'), verbose_name=_("Technical Operation"))

    external_damages = models.BooleanField(default=False, help_text=_('Is an insurance for external damages included?'), verbose_name=_("External Damages"))
    pressure_vessels = models.BooleanField(default=False, help_text=_('Is the replacement of pressure vessels included?'), verbose_name=_("Pressure Vessels"))
    overhaul_working_equipment = models.BooleanField(default=False, help_text=_('Is the general overhaul of working equipment (winch, on-board crane, etc.) included?'), verbose_name=_("Overhaul Working Equipment"))
    cms = models.BooleanField(default=False, help_text=_('Is a permanent condition monitoring included?'))

    rotor_blade_inspection = models.BooleanField(default=False, help_text=_('Are rotor blade inspections included?'), verbose_name=_("Rotor Blade Inspection"))
    videoendoscopic_inspection_gearbox = models.BooleanField(default=False, help_text=_('Are videoendoscopic inspections of the gearbox included?'), verbose_name=_("Videoendoscopic Inspection Gearbox"))
    periodic_inspection_wtg = models.BooleanField(default=False, help_text=_('Are periodic inspections of the WTG (WKP) included?'), verbose_name=_("Periodic Inspection WTG"))

    service_lift_maintenance = models.BooleanField(default=False, help_text=_('Is service lift maintenance included?'), verbose_name=_("Service Lift Maintenance"))
    safety_inspection = models.BooleanField(default=False, help_text=_('Is the inspection of safety equipment (PSE, fire extinguisher, etc.) included?'), verbose_name=_("Safety Inspection"))
    safety_repairs = models.BooleanField(default=False, help_text=_('Is the repair of safety equipment (PSE, fire extinguisher, etc.) included?'), verbose_name=_("Safety Repairs"))
    safety_exchange = models.BooleanField(default=False, help_text=_('Is the exchange of safety equipment (PSE, fire extinguisher, etc.) included?'), verbose_name=_("Safety Exchange"))

    certified_body_inspection_service_lift = models.BooleanField(default=False, help_text=_('Is the inspection of the service lift by a certified body (ZÜS) included?'), verbose_name=_("Certified Body Inspection Service Lift"))
    electrical_inspection = models.BooleanField(default=False, help_text=_('Are the electrical inspection (DGUV V3) included?'), verbose_name=_("Electrical Inspection"))

    comment = fields.GenericRelation('projects.Comment', verbose_name=_("Comment"))

    active = models.BooleanField(default=True, verbose_name=_("Actice"))
    created = models.DateField(auto_now_add=True, verbose_name=_("Created"))
    updated = models.DateField(auto_now=True, verbose_name=_("Updated"))

    class Meta:
        ordering = ['start_date']
        permissions = (("can_comment_contracts", "Can write comments on contracts."),
                        ("can_view_contract_pdf", "Can view contract pdf."),
                        ("can_terminate_contract", "Can terminate contract"),
                        ("can_create_custom_export_of_contracts", "Can create a custom export of contracts"),
                        ("change_dwt_responsible", "Can change the DWT Responsible"),
                        ("open_TO_menu", "Can open Technical Operations Menu"),)

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
        turbines = self.turbines.all()
        models = {}
        for t in turbines:
            if t.wec_typ.__str__ not in models.keys():
                models[t.wec_typ.__str__] = t.wec_typ.get_absolute_url()
        return models
    contracted_wec_types = property(_contracted_wec_types)

    def _contracted_wec_types_name(self):
        wec_types = self.turbines.all().select_related('wec_typ', 'wec_typ__manufacturer').order_by().values_list('wec_typ', flat=True).distinct()
        models = polls.models.WEC_Typ.objects.filter(id__in=wec_types).select_related('manufacturer').values_list('manufacturer__name', 'name')
        return ", ".join([" ".join(map(str,x)) for x in models])
    contracted_wec_types_name = property(_contracted_wec_types_name)

    def _contracted_oem_name(self):
        oems = list(set([str(x.wec_typ.manufacturer.name) for x in self.turbines.all()]))
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
            age = _('not defined')
        return age
    turbine_age = property(_turbine_age)

    def _contract_coordinates(self):
        if len(self.turbines.all()) > 0:
            longitude = self.turbines.all()[0].wind_farm.longitude
            latitude = self.turbines.all()[0].wind_farm.latitude
            return {'latitude': latitude, 'longitude': longitude}
        else:
            return "None"
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
        elif self.remote_control != True and self.main_components != True and self.unscheduled_maintenance_material != True and self.unscheduled_maintenance_personnel != True and self.scheduled_maintenance != True and self.technical_operation == True:
            scope = "Technical Operation"
        else:
            scope = "Other"
        if scope != "Technical Operation" and self.technical_operation == True:
            scope = scope + " & TO"
        return scope
    contract_scope = property(_contract_scope)

    def __str__(self):
        return self.name

class ServiceLocation(models.Model):
    name = models.CharField(max_length=100, db_index=True, default="Osnabrück")
    postal_code = models.CharField(max_length=20, default="49082", verbose_name=_("Postal Code"))
    dwt = models.CharField(max_length=30, choices=DWT, default='DWTX')
    location_type = models.CharField(max_length=50, choices=LOCATION, default='Vehicle', verbose_name=_("Location Type"))
    supported_technology = models.ManyToManyField('polls.Manufacturer', verbose_name=_("Supported Technology"))

    latitude = models.FloatField()
    longitude = models.FloatField()

    active = models.BooleanField(default=True, verbose_name=_("Active"))
    created = models.DateField(auto_now_add=True, verbose_name=_("Created"))
    updated = models.DateField(auto_now=True, verbose_name=_("Updated"))

    def _supported_technology_name(self):
        manufacturers = self.supported_technology.all().prefetch_related('manufacturer').values_list('name', flat=True)
        return ", ".join([str(x) for x in manufacturers])
    supported_technology_name = property(_supported_technology_name)

    def __str__(self):
        return self.name