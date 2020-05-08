from django.db import models
from django.db.models import Min, Case, When, Sum
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields
from django.utils.translation import ugettext_lazy as _
#from django.conf import settings

from datetime import date, datetime, timedelta
from math import sin, cos, sqrt, atan2, radians
from phonenumber_field.modelfields import PhoneNumberField

import polls.models
import wind_farms.models
import turbine.models

from django.contrib.auth.models import User

def get_name(self):
    return " ".join((self.first_name, self.last_name))

User.add_to_class("__str__", get_name)

STATUS = (
    ('Potential', _('Potential')),
    ('Coffee', _('Coffee')),
    ('Soft Offer', _('Soft Offer')),
    ('Hard Offer', _('Hard Offer')),
    ('Negotiation', _('Negotiation')),
    ('Final Negotiation', _('Final Negotiation')),
    ('Won', _('Won')),
    ('Lost', _('Lost')),
    ('Cancelled', _('Cancelled')),)

CONTRACT_TYPE = (
    ('Basic Maintenance', _('Basic Maintenance')),
    ('Full Maintenance without MC', _('Full Maintenance without MC')),
    ('Full Maintenance with MC', _('Full Maintenance with MC')),
    ('Remote Control', _('Remote Control')),
    ('Spare Parts', _('Spare Parts')),
    ('Technical Operation', _('Technical Operation')),
    ('Foundation works', _('Foundation works')),
    ('Subsea Foundation and Seabed works', _('Subsea Foundation and Seabed works')),
    ('Offshore sub station service', _('Offshore sub station service')),
    ('BNK', 'BNK'),
    ('Other', _('Other')),)

CONTRACT_TYPE_CQ = (
    ('Basic Maintenance', _('Basic Maintenance')),
    ('Full Maintenance without Main Components', _('Full Maintenance with Main Components')),
    ('Full Maintenance with Main Components', _('Full Maintenance with Main Components')),
    ('Remote Control', _('Remote Control')),
    ('Other', _('Other')),)

CONTRACT = (
    ('New Contract', _('New Contract')),
    ('Extension', _('Extension')),
    ('Upgrade', _('Upgrade')),
    ('Downgrade', _('Downgrade')),)

DWT = (
    ('DWTX', 'DWTX'),
    ('DWTS', 'DWTS'),
    ('DWTOC', 'DWTOC'),
    ('DWTUK', 'DWTUK'),
    ('DWTSARL', 'DWTSARL'),
    ('DWTES', 'DWTES'),
    ('DWTNED', 'DWTNED'),
    ('DWTPO', 'DWTPO'),
    ('DWTUS', 'DWTUS'),
    ('DWTAB', 'DWTAB'),
    ('DWTDK', 'DWTDK'),
    ('GFW', 'GFW'),)

DEPARTMENT = (
    ('Service', 'Service'),
    ('Technical Operations', _('Technical Operations')),)

NEW_CUSTOMER = (
    ('Yes', _('Yes')),
    ('No', _('No')),)

AWARDING_REASON = (
    ('Price', _('Price')),
    ('Contract Design', _('Contract Design')),
    ('Experience with DWT', _('Experience with DWT')),
    ('Readiness', _('Readiness')),
    ('Regional Structures', _('Regional Structures')),
    ('Political Decision', _('Political Decision')),
    ('Liability', _('Liability')),
    )

CONTRACT_SCOPE = (
    ('Service Contract', _('Service Contract')),
    ('Technical Operations Contract', _('Technical Operations Contract')),
    ('Commisioned Work', _('Commisioned Work')),
    ('Request for Material', _('Request for Material')),
    ('Support Contract', _('Support Contract')),
    )

TOWER = (
    ('Lattice Tower', _('Lattice Tower')),
    ('Tubular Tower', _('Tubular Tower')),
    )

OBSTACLE_LIGHT = (
    ('Day/Night', _('Day/Night')),
    ('Night', _('Night')),
    )

PHONE_TYPE =(
    ('ISDN', 'ISDN'),
    ('DSL', 'DSL'),
    ('VDSL', 'VDSL'),
    ('LTE', 'LTE'),
    )

questionnaire_translation_dict = {
    'Servicevertrag':'Service Contract',
    'TBF-Vertrag':'Technical Operations Contract',
    'Auftragsarbeit':'Commisioned Work',
    'Materialanfrage':'Request for Material',
    'Support-Vertrag':'Support Contract',
    'Rohrturm':'Tubular Tower',
    'Gittermastturm':'Lattice Tower',
    }

class Reminder(models.Model):
    date = models.DateField(help_text=_("The reminder is going to pop up on this specified date, which has to be in the future."), verbose_name=_("Date"))
    text = models.TextField(help_text=_("This text is going to appear in a mail which is going to be send on the the specified date to the recipient."))
    multiple_recipients = models.ManyToManyField('auth.User',verbose_name=_("Recipients"), help_text=_("Who is the reminder addressed to?"), related_name="reminder_recipients")

    limit = models.Q(app_label = 'projects', model = 'project')
    content_type = models.ForeignKey(ContentType, limit_choices_to = limit, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = fields.GenericForeignKey('content_type', 'object_id')

    created = models.DateTimeField(auto_now_add=True, db_index=True)
    created_by = models.ForeignKey('auth.User', default=7)

    class Meta:
        ordering = ('-created',)
        permissions = (("can_set_reminders", "Can set reminders."),)

    def __str__(self):
        return self.text

class Comment(models.Model):

    text = models.TextField(blank=True)
    file = models.FileField(upload_to='project_files/%Y/%m/%d/', blank=True)
    available = models.BooleanField(default=True)

    limit = models.Q(app_label = 'projects', model = 'project') | models.Q(app_label = 'projects', model = 'poolproject') | models.Q(app_label = 'player', model = 'player') | models.Q(app_label = 'player', model = 'person') | models.Q(app_label = 'polls', model = 'wec_typ') | models.Q(app_label = 'wind_farms', model = 'windfarm') | models.Q(app_label = 'turbine', model = 'turbine') | models.Q(app_label = 'turbine', model = 'contract') | models.Q(app_label = 'events', model = 'event')
    content_type = models.ForeignKey(ContentType, limit_choices_to = limit, null=True, blank=True,)
    object_id = models.PositiveIntegerField(null=True,)
    content_object = fields.GenericForeignKey('content_type', 'object_id')

    created = models.DateTimeField(auto_now_add=True, db_index=True)
    created_by = models.ForeignKey('auth.User', default=7)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.text

class Technologieverantwortlicher(models.Model):

    manufacturer = models.ForeignKey('polls.Manufacturer', related_name='technology')
    technology_responsible = models.ForeignKey('auth.User')

class OfferNumber(models.Model):
    number = models.CharField(max_length=50, db_index=True, unique=True, help_text=_("Offer Number generated automatically to ensure its uniqueness."), verbose_name=_("Number"))
    wind_farm = models.CharField(max_length=50, null=True, blank=True, help_text=_("Specify the wind farm which belongs to this offer number"), verbose_name=_("Wind Farm"))
    amount = models.PositiveIntegerField(null=True, blank=True, help_text=_("Amount of turbines included in this project."), verbose_name=_("Amount"))
    dwt = models.CharField(max_length=30, choices=DWT, default='DWTS')
    wec_typ = models.ManyToManyField('polls.WEC_Typ', verbose_name=_('Model'), blank=True, help_text=_("Enter the turbine type (e.g. V90) not the manufacturer (e.g. Vestas)!"))
    sales_manager = models.ForeignKey('auth.User', blank=True, null=True, help_text=_("Who is the responsible Sales Manager?"), verbose_name=_("Sales Manager"))
    text = models.TextField(blank=True, help_text=_("Additional information"))

    created = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name=_("Created"))
    created_by = models.ForeignKey('auth.User', related_name="offer_number_created_by", verbose_name=_("Created by"))

    class Meta:
        get_latest_by = "created"
        ordering = ('-created',)

    def relatedProject(self):
        if len(self.project_set.all()) == 1:
            project = self.project_set.all()[0].name
            return project
        elif len(self.project_set.all()) > 1:
            projects = _("Attention: Offer Number is used for multiple projects: ")
            count = 0
            for p in self.project_set.all():
                projects += p.name
                count += 1
                if count != len(self.project_set.all()):
                    projects += ", "
            return projects
        else:
            return None

    def __str__(self):
        return self.number

    def get_absolute_url(self):
        return reverse('projects:offer_number_list')

class ProjectSet(models.QuerySet):
    def add_first_commisioning(self):
        return self.annotate(first_com_date=Case(When(turbines__commisioning_year__isnull=False, then=Min('turbines__commisioning_year'))))

    def add_mw(self):
        return self.annotate(project_mw=Sum('turbines__wec_typ__output_power'))

class Project(models.Model):
    objects = ProjectSet.as_manager()

    name = models.CharField(max_length=50, db_index=True)
    slug = models.SlugField(max_length=50, db_index=True)

    offer_number = models.ForeignKey('OfferNumber', blank=True, null=True, help_text=_("Offer Number to establish a connection to written offers"), verbose_name=_("Offer Number"))

    status = models.CharField(max_length=25, choices=STATUS, default='Coffee')
    prob = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name=_('Probability [%]'), help_text=_("Estimate the probability of conclusion"))
    dwt = models.CharField(max_length=30, choices=DWT, default='DWTX', help_text=_("Which unit will this project be contracted to?"))
    tender = models.BooleanField(default=False, help_text=_("Is this project part of a tender?"), verbose_name=_("Tender"))
    turbines = models.ManyToManyField('turbine.Turbine', related_name='project_turbines', verbose_name=_('Turbines'), db_index=True, help_text=_("Assign all turbines related to this project"))
    customer = models.ForeignKey('player.Player', related_name='project_customer', help_text=_("Which company are we in touch with?"), verbose_name=_("Negotiation Partner"))
    customer_contact = models.ForeignKey('player.Person', blank=True, null=True, related_name='customer_contact_projects', help_text=_("Who is the contact person at the negetiotion partner?"), verbose_name=_("Contact Person"))

    contract = models.CharField(max_length=30, choices=CONTRACT, default='New Contract', verbose_name=_("Contract"))
    contract_type = models.CharField(max_length=30, choices=CONTRACT_TYPE, default='Contract Overview', verbose_name=_("Contract Type"))
    run_time = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('Runtime [years]'))
    sales_manager = models.ForeignKey('auth.User', related_name='sales_manager', help_text=_("Who is the responsible Sales Manager?"), verbose_name=_("Sales Manager"))
    request_date = models.DateField(default=timezone.now, blank=True, null=True, help_text=_("When was the first contact established?"), verbose_name=_("Request Date"))
    start_operation = models.DateField(blank=True, null=True, help_text=_("What is the intended contract commencement date?"), verbose_name=_("Operation Start"))
    contract_signature = models.DateField(blank=True, null=True, help_text=_("When is the contract intended to be signed?"), verbose_name=_("Contract Signature"))
    price = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('Price'), help_text=_("State the average yearly remuneration per WTG"))
    ebt = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True, verbose_name=_('EBT [%]'), help_text=_("Which margin results from the price?"))

    parkinfo = models.FileField(upload_to='project_files/parkinfoblatt/', verbose_name=_("Wind Farm Information Sheet"), blank=True)
    kundendaten = models.FileField(upload_to='project_files/kundendatenblatt/', verbose_name=_("Customer Information Sheet"), blank=True)

    zop = models.BooleanField(default=False, verbose_name=_("Condition based inspection"))
    rotor = models.BooleanField(default=False, verbose_name=_("Rotor blade inspection"))
    gearbox_endoscopy = models.BooleanField(default=False, verbose_name=_("Videoendoscopic gearbox inspection"))

    awarding_reason = models.CharField(max_length=30, choices=AWARDING_REASON, blank=True, null=True, help_text=_("Which reason lead to the awarding of the contract?"), verbose_name=_("Awarding Reason"))

    comment = fields.GenericRelation(Comment, related_query_name='comments')
    reminder = fields.GenericRelation(Reminder, related_query_name='reminders')
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        ordering = ('-updated',)
        index_together = (('id', 'slug'),)
        permissions = (("can_comment_projects", "Can write comments on Sales projects."),
                        ("can_create_project_overview", "Can create an overview of sales projects"),
                        ("can_create_custom_export", "Can create a custom export of sales projects"),
                        ("project_to_contract", "Can create contracts from won projects"),
                        ("initialization", "Can create initailization sheet"),
                        ("change_sales_manager", "Can change Sales Manager"),
                        ("open_sales_tools", "Can open Sales Tools"),)

    def _amount_turbines(self):
        project_turbines = self.turbines.all().count()
        return project_turbines
    amount_turbines = property(_amount_turbines)

    def _all_comments(self):
        comment_list = [x for x in self.comment.exclude(text__in=['created project', 'edited project'])]
        comment_str_list = []
        for c in comment_list:
            comment_str_list.append(': '.join([str(c.created), c.text]))
        comment_str = '; '.join(comment_str_list)
        return comment_str
    all_comments = property(_all_comments)

    def _last_update(self):
        last_comment = Comment.objects.filter(object_id=self.id, content_type=ContentType.objects.get(app_label = 'projects', model = 'project')).exclude(text__in=["edited project", "created_project"]).first().created.date()
        if last_comment > self.updated.date():
            last_updated = last_comment.strftime('%d %b %Y')
        else:
            last_updated = self.updated.date().strftime('%d %b %Y')
        return last_updated
    last_update = property(_last_update)

    def _mw(self):
        try:
            mw = Project.objects.add_mw().get(pk=self.pk).project_mw*0.001
            return round(mw, 2)
        except:
            return 0
    mw = property(_mw)

    def _yearly_contract_value(self):
        try:
            total = self.price * self.turbines.all().count()
        except:
            total = _("not defined")
        return total
    yearly_contract_value = property(_yearly_contract_value)

    def _total_contract_value(self):
        try:
            total = self.price * self.run_time * self.turbines.all().count()
        except:
            total = _("not defined")
        return total
    total_contract_value = property(_total_contract_value)

    def _first_commisioning(self):
        f_c = Project.objects.add_first_commisioning().get(pk=self.pk).first_com_date
        if not f_c == None:
            return f_c
        else:
            return _("not defined")
    first_commisioning = property(_first_commisioning)

    def _turbine_age(self):
        f_c = self.turbines.aggregate(first_commisioning=Case(When(commisioning_year__isnull=False, then=Min('commisioning_year'))))['first_commisioning']
        try:
            start = self.start_operation.year
        except:
            start = datetime.now().year
        if not f_c == None:
            age = start - f_c
            if age < 0:
                age = 0
            return age
        else:
            return _('not defined')
    turbine_age = property(_turbine_age)

    def _project_windfarm(self):
        windfarms = {}
        turbines = self.turbines.all().select_related('wind_farm')
        for t in turbines:
            try:
                windfarms[t.wind_farm.name] = t.wind_farm.get_absolute_url()
            except:
                pass
        return windfarms
    project_windfarm = property(_project_windfarm)

    def _project_windfarm_name(self):
        windfarms = self.project_windfarm
        windfarm_name = list(set([x for x in windfarms.keys()]))
        return ", ".join([str(x) for x in windfarm_name])
    project_windfarm_name = property(_project_windfarm_name)

    def _project_postal_codes(self):
        postal_codes = []
        turbines = self.turbines.all()
        for t in turbines:
            if t.wind_farm.postal_code not in postal_codes:
                postal_codes.append(t.wind_farm.postal_code)
        return ", ".join([str(x) for x in postal_codes])
    project_postal_codes = property(_project_postal_codes)

    def project_tbf(self):
        tbfs = []
        turbines = self.turbines.all().prefetch_related('tec_operator')
        for t in turbines:
            for tbf in t.tec_operator.all().values_list('name', flat=True):
                tbfs.append(tbf)
        tbfs = list(set(tbfs))
        return tbfs

    def _project_wec_types(self):
        turbines = self.turbines.all().select_related('wec_typ')
        models = {}
        for t in turbines:
            if t.wec_typ.__str__ not in models.keys():
                models[t.wec_typ.__str__] = t.wec_typ.get_absolute_url()
        return models
    project_wec_types = property(_project_wec_types)

    def _project_wec_types_name(self):
        wec_types = self.turbines.all().select_related('wec_typ', 'wec_typ__manufacturer').order_by().values_list('wec_typ', flat=True).distinct()
        models = polls.models.WEC_Typ.objects.filter(id__in=wec_types).select_related('manufacturer').values_list('manufacturer__name', 'name')
        return ", ".join([" ".join(map(str,x)) for x in models])
    project_wec_types_name = property(_project_wec_types_name)

    def _project_oem_name(self):
        wec_types = self.turbines.all().select_related('wec_typ', 'wec_typ__manufacturer').order_by().values_list('wec_typ__manufacturer', flat=True).distinct()
        oems = polls.models.Manufacturer.objects.filter(id__in=wec_types).values_list('name', flat=True)
        return ", ".join([str(x) for x in oems])
    project_oem_name = property(_project_oem_name)

    def _project_country(self):
        country_list = self.turbines.all().select_related('wind_farm').order_by().values_list('wind_farm__country', flat=True).distinct()
        countries = wind_farms.models.Country.objects.filter(id__in=country_list).values_list('name', flat=True)
        return ", ".join([str(x) for x in countries])
    project_country = property(_project_country)

    def _project_owner(self):
        turbines = self.turbines.all().select_related('owner')
        owners = {t.owner.name : t.owner.get_absolute_url() for t in turbines}
        return owners
    project_owner = property(_project_owner)

    def _project_owner_name(self):
        turbines = self.turbines.all().select_related('owner')
        owners = list(set([str(x.owner.name) for x in turbines if x.owner != None]))
        return ", ".join([str(x) for x in owners])
    project_owner_name = property(_project_owner_name)

    def _project_coordinates(self):
        if len(self.turbines.all()) > 0 and self.turbines.all()[0].wind_farm.longitude:
            longitude = self.turbines.all()[0].wind_farm.longitude
            latitude = self.turbines.all()[0].wind_farm.latitude
            return {'latitude': latitude, 'longitude': longitude}
        else:
            return {'latitude': -34.619497, 'longitude': 39.363809}
    project_coordinates = property(_project_coordinates)

    def _closest_service_location(self):
        R = 6373.0
        min_distance = 1000
        service_location = {'name': _("non existent"), 'distance': min_distance, 'postal_code': "49086"}
        if len(self.turbines.all()) > 0:
            lat = radians(self.turbines.all()[0].wind_farm.latitude)
            lon = radians(self.turbines.all()[0].wind_farm.longitude)
            service_stations = turbine.models.ServiceLocation.objects.filter(active=True, dwt=self.dwt, supported_technology=self.turbines.all()[0].wec_typ.manufacturer)
            for s in service_stations:
                dlon = radians(s.longitude) - lon
                dlat = radians(s.latitude) - lat
                a = sin(dlat / 2)**2 + cos(lat) * cos(radians(s.latitude)) * sin(dlon / 2)**2
                c = 2 * atan2(sqrt(a), sqrt(1 - a))
                distance = R * c
                if distance < min_distance:
                    min_distance = distance
                    service_location = {'name': s.name, 'distance': "{0:.2f}".format(round(min_distance,2)), 'postal_code': s.postal_code, 'DWT': s.dwt,}
                else:
                    pass
        return service_location
    closest_service_location = property(_closest_service_location)

    def driving_rate(self, distance, minutes):
        gas = int(distance) * 2 * 0.44
        personnel = int(minutes)/60.0 * 2 * 2 * 37
        costs = gas + personnel
        result = {'weekday': "{0:.2f}".format(round(costs,2)), 'saturday': "{0:.2f}".format(round(costs*1.5,2)), 'sunday': "{0:.2f}".format(round(costs*2,2))}
        return result

    def contracts_in_100km_distance(self, distance):
        distance = int(distance)
        R = 6373.0
        close_contracts = {}
        if len(self.turbines.all()) > 0:
            lat = radians(self.turbines.all()[0].wind_farm.latitude)
            lon = radians(self.turbines.all()[0].wind_farm.longitude)
            contracts = turbine.models.Contract.objects.filter(active=True).exclude(turbines=None)
            for contract in contracts:
                dlon = radians(contract.turbines.all()[0].wind_farm.longitude) - lon
                dlat = radians(contract.turbines.all()[0].wind_farm.latitude) - lat
                a = sin(dlat / 2)**2 + cos(lat) * cos(radians(contract.turbines.all()[0].wind_farm.latitude)) * sin(dlon / 2)**2
                b = 2 * atan2(sqrt(a), sqrt(1 - a))
                distance_c = R * b
                if distance_c < distance:
                    close_contracts[contract.contracted_windfarm_name] = {'distance': "{0:.2f}".format(round(distance_c,2)), 'url': contract.get_absolute_url()}
                else:
                    pass
        return close_contracts

    def turbines_in_distance(self, manufacturer, distance):
        distance = int(distance)
        manufacturer = int(manufacturer)
        R = 6373.0
        close_turbines = {}
        if len(self.turbines.all()) > 0:
            country = self.turbines.all()[0].wind_farm.country
            lat = radians(self.turbines.all()[0].wind_farm.latitude)
            lon = radians(self.turbines.all()[0].wind_farm.longitude)
            turbines = turbine.models.Turbine.objects.filter(available=True, wind_farm__country=country, wec_typ__manufacturer=manufacturer,latitude__isnull=False, longitude__isnull=False)
            for t in turbines:
                dlon = radians(t.longitude) - lon
                dlat = radians(t.latitude) - lat
                a = sin(dlat / 2)**2 + cos(lat) * cos(radians(t.latitude)) * sin(dlon / 2)**2
                b = 2 * atan2(sqrt(a), sqrt(1 - a))
                distance_c = R * b
                if distance_c < distance:
                    if t.wind_farm.name not in close_turbines.keys():
                        close_turbines[t.wind_farm.name] = {'distance': "{0:.2f}".format(round(distance_c,2)), 'url': t.wind_farm.get_absolute_url()}
                else:
                    pass
        return close_turbines

    def _technologieverantwortlicher(self):
        if self.dwt == "GFW":
            p = User.objects.get(username="Jürgen_Fuhrländer")
            return p.__str__()
        if self.contract_type == "Technical Operation" and self.dwt == "DWTX":
            p = User.objects.get(username="Lars")
            return p.__str__()
        else:
            oem_id = list(set([str(x.wec_typ.manufacturer.id) for x in self.turbines.all()]))
            technology_responsible = []
            for m in oem_id:
                p = Technologieverantwortlicher.objects.get(manufacturer__id=m)
                if p.technology_responsible.__str__() not in technology_responsible:
                    technology_responsible.append(p.technology_responsible.__str__())
            return ", ".join(technology_responsible)
    technologieverantwortlicher = property(_technologieverantwortlicher)

    def _warning_info(self):
        if self.start_operation != None:
            days_to_start = self.start_operation - date.today()
        else:
            days_to_start = timedelta(days=31)
        if self.dwt in ["DWTX", "DWTSARL"] and self.status in ["Negotiation", "Final Negotiation", "Won"] and days_to_start.days < 30 and (self.kundendaten == "" or self.parkinfo == ""):
            return 'red'
        else:
            return 'no'
    warning_info = property(_warning_info)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('projects:project_detail', args=[self.id, self.slug])

class PoolProject(models.Model):

    name = models.CharField(max_length=50, db_index=True)
    slug = models.SlugField(max_length=50, db_index=True)
    projects = models.ManyToManyField('projects.Project', db_index=True, help_text=_("Assign all projects related to this Pool Project"), verbose_name=_("Projects"), related_name="pool_projects")

    customer = models.ForeignKey('player.Player', related_name='pool_customer', help_text=_("Which company are we in touch with?"), verbose_name=_("Negotiation Partner"))
    customer_contact = models.ForeignKey('player.Person', blank=True, null=True, related_name='customer_contact_pool', help_text=_("Who is the contact person at the negetiotion partner?"), verbose_name=_("Contact Person"))

    sales_manager = models.ForeignKey('auth.User', help_text=_("Who is the responsible Sales Manager?"), verbose_name=_("Sales manager"), related_name="pool_sales_manager")
    request_date = models.DateField(default=timezone.now, blank=True, null=True, help_text=_("When was the first contact established?"), verbose_name=_("Request Date"))

    comment = fields.GenericRelation(Comment, related_query_name='pool_comments')
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, db_index=True)
    changed_by = models.ForeignKey('auth.User', default=7, related_name="pool_changed_by")

    class Meta:
        ordering = ('-updated',)
        index_together = (('id', 'slug'),)

    def _amount_projects(self):
        pool_projects = self.projects.all().count()
        return pool_projects
    amount_projects = property(_amount_projects)

    def _pool_projects(self):
        projects = self.projects.all()
        projects = list(set([str(x) for x in projects]))
        if len(projects) == 1:
            return projects[0]
        else:
            return ", ".join([str(x) for x in projects])
    pool_projects = property(_pool_projects)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('projects:pool_detail', args=[self.id, self.slug])

class Calculation_Tool(models.Model):
    file = models.FileField(upload_to='calculation_tool/%Y/%m/%d/')
    valid_for_country = models.ManyToManyField('wind_farms.Country')
    version = models.CharField(max_length=8)
    created = models.DateTimeField(auto_now_add=True)

    def _country_names(self):
        countries = self.valid_for_country.all().values_list('name', flat=True)
        countries_str = ", ".join(countries)
        return countries_str
    country_names = property(_country_names)

    def __str__(self):
        return "_".join(("Calculation_Tool_v", self.version))

class Document(models.Model):
    title = models.CharField(max_length=50)
    file = models.FileField(upload_to='document/%Y/%m/%d/')
    version = models.CharField(max_length=8)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title

class CustomerQuestionnaire(models.Model):
    #contact data
    contact_company = models.CharField(max_length=80, help_text=_("Please enter name of your employer including type of business i.e. ltd. or GmbH & Co. KG"), verbose_name=_("Company"))
    contact_name = models.CharField(max_length=80, help_text=_("Please enter your first and last name."), verbose_name=_("Name"))
    contact_position = models.CharField(max_length=80, blank=True, help_text=_("Please indicate your position in the company."), verbose_name=_("Position"))
    contact_mail = models.EmailField(max_length=80, help_text=_("Please enter your mail address"))
    confirm_data_security = models.BooleanField(default=False)

    # base data
    scope = models.CharField(max_length=30, choices=CONTRACT_SCOPE, default='Service Contract', help_text=_("Please choose your prefered scope."), verbose_name=_("Desired Scope"))
    wind_farm_name = models.CharField(max_length=80, help_text=_("If several wind farm names exist, please name all of them."), verbose_name=_("Wind Farm Name"))
    street_nr = models.CharField(max_length=50, blank=True, verbose_name=_("Street Number"), help_text=_("Please enter the street and if possible the house number of the location of the wind farm"))
    postal_code = models.CharField(max_length=20, blank=True, verbose_name=_("Postal Code"), help_text=_("Please enter the postal code of the location of the wind farm"))
    city = models.CharField(max_length=80, blank=True, help_text=_("Please name the village where the wind farm is located."), verbose_name=_("City"))
    location_details = models.CharField(max_length=200, blank=True, help_text=_("Here you can enter additional information on the location of the wind farm."), verbose_name=_("Location"))
    amount_wec = models.PositiveIntegerField(null=True, help_text=_("Please state the number of relevant WTG."), verbose_name=_("Amount of Turbines"))

    #contractual partner data
    contractual_partner = models.CharField(max_length=50, blank=True, verbose_name=_("Contractual Partner"), help_text=_("Please indicate the complete name of the contractual partner."))
    cp_street_nr = models.CharField(max_length=50, blank=True, help_text=_("Please enter street name and number of the contractual partner."))
    cp_postal_code = models.CharField(max_length=20, blank=True, help_text=_("Please enter post code of the contractual partner."))
    cp_city = models.CharField(max_length=80, blank=True, help_text=_("Please enter city of the contractual partner."))
    cp_contact_person = models.CharField(max_length=100, blank=True, help_text=_("Please indicate first and last name of a contact person."))
    cp_phone = PhoneNumberField(blank=True, help_text=_("Please enter the phone number of the contact person in the format '+49 541 38 05 38 100'."))
    cp_mail = models.EmailField(max_length=80, blank=True, help_text=_("Please enter the email address of the contact person"))
    cp_legal_form = models.CharField(max_length=50, blank=True, help_text=_("Please indicate the correct type of business of the contractual partner i.e. ltd. or GmbH & Co. KG."))

    #Person vor Ort / Mühlenwart
    authorized_person_on_site = models.CharField(max_length=50, blank=True, help_text=_("Please indicate (if existing) the complete name of a local hand for the windfarm. "), verbose_name=_("Local hand on site"))
    ap_street_nr = models.CharField(max_length=50, blank=True, help_text=_("Please enter street name and number of your local hand."))
    ap_postal_code = models.CharField(max_length=20, blank=True, help_text=_("Please enter post code of your local hand."))
    ap_city = models.CharField(max_length=80, blank=True, help_text=_("Please enter city of your local hand."))
    ap_contact_person = models.CharField(max_length=100, blank=True)
    ap_phone = PhoneNumberField(blank=True, help_text=_("Please enter the phone number of your local hand in the format '+49 541 38 05 38 100'."))
    ap_mail = models.EmailField(max_length=80, blank=True, help_text=_("Please enter the email address of your local hand."))

    #invoice recipient
    invoice_recipient = models.CharField(max_length=50, blank=True, verbose_name=_("Invoice Recipient"), help_text=_("Please enter the full company name of the invoice receipient."))
    ir_street_nr = models.CharField(max_length=50, blank=True, help_text=_("Please enter street name and number of the invoice recipient."))
    ir_postal_code = models.CharField(max_length=20, blank=True, help_text=_("Please enter post code of the invoice recipient."))
    ir_city = models.CharField(max_length=80, blank=True, help_text=_("Please enter city of the invoice recipient."))
    ir_contact_person = models.CharField(max_length=100, blank=True, help_text=_("Please indicate first and last name of a contact person at the financial department of the invoice receipient."))
    ir_phone = PhoneNumberField(blank=True, help_text=_("Please enter the phone number of the contact person in the format '+49 541 38 05 38 100'."))
    ir_mail = models.EmailField(max_length=80, blank=True, help_text=_("Please enter the email address of the contact person at the financial department."))
    ir_tax_id = models.CharField(max_length=20, blank=True, help_text=_("Please indicate value added tax ID number."))
    ir_invoice_mail = models.EmailField(max_length=80, blank=True, help_text=_("Please enter the email address to which invoices shall be send in future."))

    #bank data
    bank_institute = models.CharField(max_length=50, blank=True, verbose_name=_("Bank Institute"), help_text=_("Please indicate the name of the relevant bank."))
    iban = models.CharField(max_length=34, blank=True, help_text=_("Please indicate IBAN."))
    bic = models.CharField(max_length=11, blank=True, help_text=_("Please indicate BIC"))
    vat_nr = models.CharField(max_length=50, blank=True)

    #shipping address
    sa_company = models.CharField(max_length=50, blank=True, verbose_name=_("Recipient"), help_text=_("Please enter the full (company) name of the shipping recipient."))
    sa_street_nr = models.CharField(max_length=50, blank=True, help_text=_("Please enter street name and number of the shipping address."))
    sa_postal_code = models.CharField(max_length=20, blank=True, help_text=_("Please enter post code of the shipping address."))
    sa_city = models.CharField(max_length=80, blank=True, help_text=_("Please enter city of the shipping address."))
    sa_information = models.CharField(max_length=200, blank=True, help_text=_("Here you can enter additional information on the shipping address."))

    #commercial operations
    commercial_operator = models.CharField(max_length=50, blank=True, verbose_name=_("Commercial Operator"), help_text=_("Please enter the full company name of the commercial operations manager."))
    co_street_nr = models.CharField(max_length=50, blank=True, help_text=_("Please enter street name and number of your commercial operations manager."))
    co_postal_code = models.CharField(max_length=20, blank=True, help_text=_("Please enter post code of your commercial operations manager."))
    co_city = models.CharField(max_length=80, blank=True, help_text=_("Please enter city of your commercial operations manager."))
    co_contact_person = models.CharField(max_length=100, blank=True, help_text=_("Please indicate first and last name of  the commercial operations manager"))
    co_phone = PhoneNumberField(blank=True, help_text=_("Please enter the phone number of the commercial operations manager in the format '+49 541 38 05 38 100'."))
    co_mail = models.EmailField(max_length=80, blank=True, help_text=_("Please enter the email address of the commercial operations manager."))

    #technical operations
    technical_operator = models.CharField(max_length=50, blank=True, verbose_name=_("Technical Operator"), help_text=_("Please enter the full company name of the technical operations manager."))
    to_street_nr = models.CharField(max_length=50, blank=True, help_text=_("Please enter street name and number of the technical operations manager."))
    to_postal_code = models.CharField(max_length=20, blank=True, help_text=_("Please enter post code of your technical operations manager."))
    to_city = models.CharField(max_length=80, blank=True, help_text=_("Please enter city of your technical operations manager."))
    to_contact_person = models.CharField(max_length=100, blank=True, help_text=_("Please indicate first and last name of a contact person at the technical operations manager."))
    to_phone = PhoneNumberField(blank=True, help_text=_("Please enter the phone number of the contact person in the format '+49 541 38 05 38 100'."))
    to_mail = models.EmailField(max_length=80, blank=True, help_text=_("Please enter the email address of the technical operations manager."))

    #service contract
    current_service_contract = models.CharField(max_length=50, blank=True, help_text=_("Kindly let us know about your current type of service agreement (full maintenance, time and material or others)."), verbose_name=_("Current service contract"))
    commencement_current_service_contract = models.DateField(blank=True, null=True, verbose_name=_("Expiry of current service contract"), help_text=_('Kindly provide the expiry date of your current contract.'))
    desired_service_contract = models.CharField(max_length=50, blank=True, choices=CONTRACT_TYPE_CQ, help_text=_("Kindly indicate your desired scope of services."),verbose_name=_("Desired service contract scope"))
    desired_duration_service_contract = models.PositiveIntegerField(blank=True, null=True, help_text=_("Please indicate the desired duration of the service contract in years."), verbose_name=_("Desired duration of service contract"))

    #documentation
    key_safe_location = models.CharField(max_length=80, blank=True, help_text=_("Where can the key for the WTG be found?"),verbose_name=_("Key Safe Location"))
    key_safe_code = models.CharField(max_length=10, blank=True, help_text=_("If a key safe is installed kindly povide access code."), verbose_name=_("Key Safe Code"))
    alarm_system = models.BooleanField(default=False, help_text=_("Is an alarm system installed? If yes, kindly check the box."), verbose_name=_("Alarm System"))
    alarm_system_information = models.CharField(max_length=80, blank=True, help_text=_("Please provide further information about the alarm system."), verbose_name=_("Alarm System Specification"))
    roadmap = models.FileField(blank=True, upload_to='customer_questionnaire/roadmap/', verbose_name=_("Roadmap"), help_text=_("Kindly upload a map showing the location and access to the wind farm."))
    single_line_diagram = models.FileField(blank=True, upload_to='customer_questionnaire/single_line_diagram/', verbose_name=_("Single Line Diagram"), help_text=_("Kindly upload a single line diagram of the wind farm."))

    #communication
    direct_marketing = models.BooleanField(default=False, help_text=_("Is the wind farm in direct marketing? If yes, kindly check the box."), verbose_name=_("Direct marketing"))
    direct_marketer = models.CharField(max_length=30, help_text=_("Please give the name of the company."), blank=True, verbose_name=_("Direct Marketer"))
    metering_point = models.CharField(max_length=30, help_text=_("Please state the meter number of the 4-quadrant meter."), blank=True, verbose_name=_("Metering Point"))
    it_contact_person = models.CharField(max_length=100, blank=True, verbose_name=_('IT Contact Person'), help_text=_('Please give name and contact details of a person who could provide detailed information about the IT infrastructure of the wind farm.'))
    it_phone = PhoneNumberField(blank=True, help_text=_("Please enter the phone number of a person who could provide detailed information about the IT infrastructure of the wind farm."), verbose_name=_('Phone'))
    it_mail = models.EmailField(max_length=80, blank=True, verbose_name=_('Mail'), help_text=_("Please enter the mail address of a person who could provide detailed information about the IT infrastructure of the wind farm."))
    substation = models.CharField(max_length=50, blank=True, help_text=_("To which grid station is the wind farm connected? - Kindly indicate the name of the grid station."), verbose_name=_("Substation"))
    grid_operator = models.CharField(max_length=50, blank=True, help_text=_("Which company operates the electricity grid? Please give name of the utility."), verbose_name=_("Grid operator"))

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        permissions = (("non_customer_view", "Can view all menues."),)

    def __str__(self):
        return str(self.id)

class Turbine_CustomerQuestionnaire(models.Model):

    # base data wec
    customer_questionnaire = models.ForeignKey(CustomerQuestionnaire, verbose_name=_("Customer Questionnaire"))
    turbine_id = models.CharField(max_length=25, blank=True, help_text=_("Please indicate the serial number of the WTG."), verbose_name=_("Turbine ID"))
    comissioning = models.DateField(blank=True, null=True, verbose_name=_("Date of comissioning"), help_text=_('Kindly provide the commissioning date of the individual WTG.'))

    manufacturer = models.ForeignKey('polls.Manufacturer', blank=True, null=True, help_text=_("Please select the manufacturer of the turbine."), verbose_name=_("Manufacturer"))
    turbine_model = models.ForeignKey('polls.WEC_Typ', blank=True, null=True, help_text=_("Please indicate the type of WTG (e.g. V90, N117 or 3.4M)."), verbose_name=_("Turbine Model"))

    output_power = models.IntegerField(blank=True, null=True, verbose_name=_('Output power'), help_text=_("Please enter the WTG capacity in kW."))
    control_system = models.CharField(max_length=30, blank=True, verbose_name=_("Control system"), help_text=_('Kindly state which type of  turbine controller is installed.'))

    latitude = models.FloatField(blank=True, null=True, help_text=_("Please provide geo coodinates for latitude of the WTG accordingly."), verbose_name=_("Latitude"))
    longitude = models.FloatField(blank=True, null=True, help_text=_("Please provide geo coodinates for longitude of the WTG accordingly."), verbose_name=_("Longitude"))

    tower_type = models.CharField(max_length=20, blank=True, choices=TOWER, help_text=_("Please specify the tower type."), verbose_name=_("Type of tower"))
    hub_height = models.DecimalField(max_digits=5, blank=True, null=True, decimal_places=1, help_text=_('Please provide the hub height in meters.'), verbose_name=_("Hub Height"))

    service_lift = models.BooleanField(default=False, help_text=_("Is a service lift installed? If yes, kindly check the box."), verbose_name=_("Service Lift"))
    service_lift_type = models.CharField(max_length=30, blank=True, help_text=_("Kindly indicate which type of service lift is installed."), verbose_name=_("Type of Service Lift"))

    ladder = models.CharField(max_length=40, blank=True, help_text=_("Please indicate the manufacturer of the ladder."), verbose_name=_("Ladder"))
    arrester_system = models.CharField(max_length=40, blank=True, help_text=_("Please specify the arrester system."), verbose_name=_("Arrester System"))


    #further data
    cms = models.BooleanField(default=False, help_text=_("Is a condition monitoring system installed? If yes, kindly check the box."))
    cms_type = models.CharField(max_length=30, blank=True, help_text=_("Please enter the type of the installed CMS."), verbose_name=_("Type of CMS"))

    ice_sensor = models.BooleanField(default=False, help_text=_("Is an ice detection system installed? If yes, kindly check the box."), verbose_name=_("Ice detection system"))
    ice_sensor_type = models.CharField(max_length=30, blank=True, help_text=_("Please enter the type of the installed ice detection system."), verbose_name=_("Type of ice detection system"))

    flicker_detection = models.BooleanField(default=False, help_text=_("Is a shadow casting detection system installed? If yes, kindly check the box."), verbose_name=_("Shadow casting detection system"))
    flicker_detection_type = models.CharField(max_length=30, blank=True, help_text=_("Please indicate the type of shadow casting detection system."), verbose_name=_("Type of shadow casting detection system"))

    obstacle_light_system = models.BooleanField(default=False, help_text=_("Is a obstruction light installed? If yes, kindly check the box."), verbose_name=_("Obstruction light system"))
    obstacle_light_manufacturer = models.CharField(max_length=30, blank=True, help_text=_("Please specify the manufacturer of the installed obstruction light."), verbose_name=_("Manufacturer of obstruction light system"))
    obstacle_light_type = models.CharField(max_length=20, blank=True, choices=OBSTACLE_LIGHT, help_text=_("Please indicate the type of the installed obstruction lights system."), verbose_name=_("Type of obstruction light system"))

    antenna = models.BooleanField(default=False, help_text=_("Is an antenna (mobile communication or radio relay) installed? If yes, kindly check the box."), verbose_name="Antenna")
    antenna_type = models.CharField(max_length=40, blank=True, help_text=_("Please specify the type of the installed antenna. "), verbose_name=_("Type of Antenna"))

    feed_in_tarif = models.DecimalField(max_digits=4, blank=True, null=True, decimal_places=3, help_text=_('Please state the feed-in tariff in €/kWh.'), verbose_name=_("Feed-in-tarif"))
    sdl = models.BooleanField(default=False, help_text=_("Only for WTG in Germany: Has the WTG been approved for 'System Dienstleistungs Bonus - SDL '?"), verbose_name="SDL")

    recent_maintenance = models.CharField(max_length=40, blank=True, help_text=_("Specify the last performed type of maintenance  (type 2/3/4)."), verbose_name=_("Recently performed maintenance"))
    date_of_recent_maintenance = models.DateField(blank=True, null=True, verbose_name=_("Date of recently performed maintenance"), help_text=_('When was the last maintenance performed?'))
    date_of_5_year_maintenance = models.DateField(blank=True, null=True, verbose_name=_("Date of recently performed 5-year-maintenance"), help_text=_('When was the last 5-year maintenance performed?'))
    date_of_transformer_maintenance = models.DateField(blank=True, null=True, verbose_name=_("Date of recently performed transformer maintenance"), help_text=_('When was the last transformer maintenance performed?'))
    date_of_converter_maintenance = models.DateField(blank=True, null=True, verbose_name=_("Date of recently performed converter maintenance"), help_text=_('When was the last converter maintenance  performed?'))
    date_of_lattice_maintenance = models.DateField(blank=True, null=True, verbose_name=_("Date of recently performed lattice tower maintenance"), help_text=_('If applicalble: When was the last lattice tower maintenance.'))
    date_of_overhaul_winch = models.DateField(blank=True, null=True, verbose_name=_("Date of recently performed general overhaul of service lift winch"), help_text=_('When was the general inspection of the Service Lift Winch carried out?'))

    date_cb_inspection_machine_tower = models.DateField(blank=True, null=True, verbose_name=_("Date of recently performed condition based inspection of machine and tower"), help_text=_('When was the last condition-based inspection of machine and tower performed?'))
    date_recurring_inspection = models.DateField(blank=True, null=True, verbose_name=_("Date of recently performed routine inspection"), help_text=_('When was the last routine inspection performed?'))
    date_rotor_blade_inspection = models.DateField(blank=True, null=True, verbose_name=_("Date of recently performed rotor blade inspection"), help_text=_('When was the last Inspection of the rotor blades performed?'))
    date_gearbox_endoscopy = models.DateField(blank=True, null=True, verbose_name=_("Date of recently performed videoendoscopic inspection of gear box"), help_text=_('When was the last video endoscopy of the gearbox performed?'))
    date_safety_inspection = models.DateField(blank=True, null=True, verbose_name=_("Date of recently performed safety inspection"), help_text=_('When was the last safety inspection carried out?'))
    date_service_lift_maintenance = models.DateField(blank=True, null=True, verbose_name=_("Date of recently performed maintenance of service lift"), help_text=_('When was the last service lift maintenance performed?'))
    date_service_lift_inspection = models.DateField(blank=True, null=True, verbose_name=_("Date of recently performed service lift inspection"), help_text=_('When was the last service lift inspection performed?'))
    date_electric_inspection = models.DateField(blank=True, null=True, verbose_name=_("Date of recently performed electric inspection"), help_text=_('When was the last electrical inspection carried out?'))
    date_blade_bearing_inspection = models.DateField(blank=True, null=True, verbose_name=_("Date of recently performed blade bearing inspection"), help_text=_('When was the last rotor blade bearing inspection performed?'))

    date_oil_exchange_main_bearing = models.DateField(blank=True, null=True, verbose_name=_("Date of recently performed oil exchange: main bearing"), help_text=_('When was the last oil/grease exchange on the main bearing performed?'))
    oil_type_main_bearing = models.CharField(max_length=40, help_text=_("Please state the name of the used oil/grease type for the main bearing."), blank=True, verbose_name=_("Used oil type for main bearing"))
    date_oil_exchange_yaw_gearbox = models.DateField(blank=True, null=True, verbose_name=_("Date of recently performed oil exchange: yaw gear"), help_text=_('When was the last oil exchange on the yaw gear performed?'))
    oil_type_yaw_gearbox = models.CharField(max_length=40, blank=True, help_text=_("Please state the name of the used type of oil for the yaw gear."), verbose_name=_("Used oil type for yaw gear"))
    date_oil_exchange_yaw_bearing = models.DateField(blank=True, null=True, verbose_name=_("Date of recently performed oil exchange: yaw bearing"), help_text=_('When was the last oil exchange on the yaw bearing performed?'))
    oil_type_yaw_bearing = models.CharField(max_length=40, blank=True, help_text=_("Please state the name of the used type of oil for the yaw bearing."), verbose_name=_("Used oil type for yaw bearing"))
    date_oil_exchange_pitch_gearbox = models.DateField(blank=True, null=True, verbose_name=_("Date of recently performed oil exchange: pitch gearbox"), help_text=_('When was the last oil exchange on the pitch gear performed?'))
    oil_type_pitch_gearbox = models.CharField(max_length=40, blank=True, help_text=_("Please state the name of the used type of oil for the pitch gear."), verbose_name=_("Used oil type for pitch gear"))
    date_oil_exchange_hydraulic = models.DateField(blank=True, null=True, verbose_name=_("Date of recently performed oil exchange: hydraulics"), help_text=_('When was the last oil exchange of hydraulic System performed?'))
    oil_type_hydraulic = models.CharField(max_length=40, blank=True, help_text=_("Please state the name of the used type of oil for the hydraulic system."), verbose_name=_("Used oil type for hydraulics"))

    expert_report = models.FileField(blank=True, upload_to='customer_questionnaire/expert_reports/', verbose_name=_("Expert Report"), help_text=_("Kindly upload the current expert inspection report of the WTG"))

    yearly_production_1 = models.DecimalField(max_digits=9, blank=True, null=True, decimal_places=1, help_text=_('Kindly provide the production data of the last year in kWh.'), verbose_name=_("Yearly Production 1"))
    yearly_production_2 = models.DecimalField(max_digits=9, blank=True, null=True, decimal_places=1, help_text=_('Kindly provide the production data two years ago in kWh.'), verbose_name=_("Yearly Production 2"))
    yearly_production_3 = models.DecimalField(max_digits=9, blank=True, null=True, decimal_places=1, help_text=_('Kindly provide the production data three years ago in kWh.'), verbose_name=_("Yearly Production 3"))

    gearbox_manufacturer = models.CharField(max_length=40, blank=True, help_text=_("Please specify the manufacturer of the gear box."), verbose_name=_("Manufacturer of gearbox"))
    gearbox_type = models.CharField(max_length=40, blank=True, help_text=_("Please indicate the installed type of gear box."), verbose_name=_("Type of gearbox"))
    gearbox_serialnr = models.CharField(max_length=40, blank=True, help_text=_("Please enter the serial number of the installed gear unit."), verbose_name=_("Serial number of gearbox"))
    gearbox_exchange = models.BooleanField(default=False, help_text=_("Has the gear unit already been replaced or overhauled? If yes, kindly check the box."))
    gearbox_year = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('Year of gearbox replacement/overhaul'), help_text=_("In which year was the gearbox replaced/reconditioned?"))

    generator_manufacturer = models.CharField(max_length=40, blank=True, help_text=_("Please specify the manufacturer of the installed generator."), verbose_name=_("Manufacturer of generator"))
    generator_type = models.CharField(max_length=40, blank=True, help_text=_("Please specify the type of the installed generator."), verbose_name=_("Type of generator"))
    generator_serialnr = models.CharField(max_length=40, blank=True, help_text=_("Please enter the serial number of the installed generator."), verbose_name=_("Serial number of generator"))
    generator_exchange = models.BooleanField(default=False, help_text=_("Has the generator already been replaced or overhauled? If yes, kindly check the box."))
    generator_year = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('Year of generator replacement/overhaul'), help_text=_("In which year was the generator replaced/reconditioned?"))

    rotor_blade_manufacturer = models.CharField(max_length=40, blank=True, help_text=_("Please indicate the manufacturer of the installed rotor blades."), verbose_name=_("Manufacturer of rotor blades"))
    rotor_blade_type = models.CharField(max_length=40, blank=True, help_text=_("Please indicate the type of the installed rotor blades."), verbose_name=_("Type of rotor blades"))
    rotor_blade_serialnr = models.CharField(max_length=40, blank=True, help_text=_("Please enter the serial number of the installed rotor blades."), verbose_name=_("Serial number of rotor blades"))
    rotor_blade_exchange = models.BooleanField(default=False, help_text=_("Have the rotor blades already been replaced or overhauled? If yes, kindly check the box."))
    rotor_blade_year = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('Year of rotor blade replacement/overhaul'), help_text=_("In which year were the rotor blades replaced/reconditioned?"))

    converter_manufacturer = models.CharField(max_length=40, blank=True, help_text=_("Please specify the manufacturer of the installed converter."), verbose_name=_("Manufacturer of converter"))
    converter_type = models.CharField(max_length=40, blank=True, help_text=_("Please specify the type of the installed converter."), verbose_name=_("Type of converter"))
    converter_serialnr = models.CharField(max_length=40, blank=True, help_text=_("Please enter the serial number of the installed converter."), verbose_name=_("Serial number of converter"))
    converter_exchange = models.BooleanField(default=False, help_text=_("Has the converter already been replaced or overhauled? If yes, kindly check the box."))
    converter_year = models.PositiveIntegerField(blank=True, null=True, verbose_name=_('Year of converter replacement/overhaul'), help_text=_("In which year was the converterr replaced/reconditioned?"))



    def __str__(self):
        return str(self.id)
