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
    ('Potential', 'Potential'),
    ('Coffee', 'Coffee'),
    ('Soft Offer', 'Soft Offer'),
    ('Hard Offer', 'Hard Offer'),
    ('Negotiation', 'Negotiation'),
    ('Final Negotiation', 'Final Negotiation'),
    ('Won', 'Won'),
    ('Lost', 'Lost'),
    ('Cancelled', 'Cancelled'),)

CONTRACT_TYPE = (
    ('Basic Maintenance', 'Basic Maintenance'),
    ('Full Maintenance without MC', 'Full Maintenance without MC'),
    ('Full Maintenance with MC', 'Full Maintenance with MC'),
    ('Remote Control', 'Remote Control'),
    ('Spare Parts', 'Spare Parts'),
    ('Technical Operation', 'Technical Operation'),
    ('Foundation works', 'Foundation works'),
    ('Subsea Foundation and Seabed works', 'Subsea Foundation and Seabed works'),
    ('Offshore sub station service', 'Offshore sub station service'),
    ('BNK', 'BNK'),
    ('Other', 'Other'),)

CONTRACT = (
    ('New Contract', 'New Contract'),
    ('Extension', 'Extension'),
    ('Upgrade', 'Upgrade'),
    ('Downgrade', 'Downgrade'),)

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
    ('Technical Operations', 'Technical Operations'),)

NEW_CUSTOMER = (
    (_('Yes'), _('Yes')),
    (_('No'), _('No')),)

AWARDING_REASON = (
    (_('Price'), _('Price')),
    (_('Contract Design'), _('Contract Design')),
    (_('Experience with DWT'), _('Experience with DWT')),
    (_('Readiness'), _('Readiness')),
    (_('Regional Structures'), _('Regional Structures')),
    (_('Political Decision'), _('Political Decision')),
    (_('Liability'), _('Liability')),
    )

CONTRACT_SCOPE = (
    (_('Service Contract'), _('Service Contract')),
    (_('Technical Operations Contract'), _('Technical Operations Contract')),
    (_('Commisioned Work'), _('Commisioned Work')),
    (_('Request for Material'), _('Request for Material')),
    (_('Support Contract'), _('Support Contract')),
    )

TOWER = (
    (_('Lattice Tower'), _('Lattice Tower')),
    (_('Tubular Tower'), _('Tubular Tower')),
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
    date = models.DateField(help_text="The reminder is going to pop up on this specified date, which has to be in the future.")
    text = models.TextField(help_text="This text is going to appear in a mail which is going to be send on the the specified date to the recipient.")
    multiple_recipients = models.ManyToManyField('auth.User',verbose_name="Recipients", help_text="Who is the reminder addressed to?", related_name="reminder_recipients")

    limit = models.Q(app_label = 'projects', model = 'project')
    content_type = models.ForeignKey(ContentType, limit_choices_to = limit, null=True, blank=True,)
    object_id = models.PositiveIntegerField(null=True,)
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
    number = models.CharField(max_length=50, db_index=True, unique=True, help_text="Offer Number generated automatically to ensure its uniqueness.")
    wind_farm = models.CharField(max_length=50, null=True, blank=True, help_text="Specify the wind farm which belongs to this offer number")
    amount = models.PositiveIntegerField(null=True, blank=True, help_text="Amount of turbines included in this project.")
    dwt = models.CharField(max_length=30, choices=DWT, default='DWTS')
    wec_typ = models.ManyToManyField('polls.WEC_Typ', verbose_name='Model', blank=True, help_text="Enter the turbine type (e.g. V90) not the manufacturer (e.g. Vestas)!")
    sales_manager = models.ForeignKey('auth.User', blank=True, null=True, help_text="Who is the responsible Sales Manager?")
    text = models.TextField(blank=True, help_text="Additional information")

    created = models.DateTimeField(auto_now_add=True, db_index=True)
    created_by = models.ForeignKey('auth.User', related_name="offer_number_created_by")

    class Meta:
        get_latest_by = "created"
        ordering = ('-created',)

    def relatedProject(self):
        if len(self.project_set.all()) == 1:
            project = self.project_set.all()[0].name
            return project
        elif len(self.project_set.all()) > 1:
            projects = "Attention: Offer Number is used for multiple projects: "
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

    offer_number = models.ForeignKey('OfferNumber', blank=True, null=True, help_text="Offer Number to establish a connection to written offers")

    status = models.CharField(max_length=25, choices=STATUS, default='Coffee')
    prob = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Probability [%]', help_text="Estimate the probability of conclusion")
    dwt = models.CharField(max_length=30, choices=DWT, default='DWTX', help_text="Which unit will this project be contracted to?")
    tender = models.BooleanField(default=False, help_text=_("Is this project part of a tender?"))
    turbines = models.ManyToManyField('turbine.Turbine', related_name='project_turbines', verbose_name='Turbines', db_index=True, help_text="Assign all turbines related to this project")
    customer = models.ForeignKey('player.Player', related_name='project_customer', help_text="Which company are we in touch with?", verbose_name="Negotiation Partner")
    customer_contact = models.ForeignKey('player.Person', blank=True, null=True, related_name='customer_contact_projects', help_text="Who is the contact person at the negetiotion partner?", verbose_name="Contact Person")

    contract = models.CharField(max_length=30, choices=CONTRACT, default='New Contract')
    contract_type = models.CharField(max_length=30, choices=CONTRACT_TYPE, default='Contract Overview')
    run_time = models.IntegerField(blank=True, null=True, verbose_name='Runtime [years]')
    sales_manager = models.ForeignKey('auth.User', related_name='sales_manager', help_text="Who is the responsible Sales Manager?")
    request_date = models.DateField(default=timezone.now, blank=True, null=True, help_text="When was the first contact established?")
    start_operation = models.DateField(blank=True, null=True, help_text=" What is the intended contract commencement date?")
    contract_signature = models.DateField(blank=True, null=True, help_text="When is the contract intended to be signed?")
    price = models.IntegerField(blank=True, null=True, verbose_name='Price', help_text="State the average yearly remuneration per WTG")
    ebt = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True, verbose_name='EBT [%]', help_text="Which margin results from the price?")

    parkinfo = models.FileField(upload_to='project_files/parkinfoblatt/', verbose_name="Wind Farm Information Sheet", blank=True)
    kundendaten = models.FileField(upload_to='project_files/kundendatenblatt/', verbose_name="Customer Information Sheet", blank=True)

    zop = models.BooleanField(default=False)
    rotor = models.BooleanField(default=False)
    gearbox_endoscopy = models.BooleanField(default=False)

    awarding_reason = models.CharField(max_length=30, choices=AWARDING_REASON, blank=True, null=True, help_text="Which reason lead to the awarding of the contract?")

    comment = fields.GenericRelation(Comment, related_query_name='comments')
    reminder = fields.GenericRelation(Reminder, related_query_name='reminders')
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, db_index=True)
    changed_by = models.ForeignKey('auth.User', default=7)

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
            total = "not defined"
        return total
    yearly_contract_value = property(_yearly_contract_value)

    def _total_contract_value(self):
        try:
            total = self.price * self.run_time * self.turbines.all().count()
        except:
            total = "not defined"
        return total
    total_contract_value = property(_total_contract_value)

    def _first_commisioning(self):
        f_c = Project.objects.add_first_commisioning().get(pk=self.pk).first_com_date
        if not f_c == None:
            return f_c
        else:
            return "not defined"
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
            return 'not defined'
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
        service_location = {'name': "non existent", 'distance': min_distance, 'postal_code': "49086"}
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
    projects = models.ManyToManyField('projects.Project', db_index=True, help_text="Assign all projects related to this Pool Project", related_name="pool_projects")

    customer = models.ForeignKey('player.Player', related_name='pool_customer', help_text="Which company are we in touch with?", verbose_name="Negotiation Partner")
    customer_contact = models.ForeignKey('player.Person', blank=True, null=True, related_name='customer_contact_pool', help_text="Who is the contact person at the negetiotion partner?", verbose_name="Contact Person")

    sales_manager = models.ForeignKey('auth.User', help_text="Who is the responsible Sales Manager?", related_name="pool_sales_manager")
    request_date = models.DateField(default=timezone.now, blank=True, null=True, help_text="When was the first contact established?")

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
    contact_company = models.CharField(max_length=80, help_text=_("Please specify the company you work for"))
    contact_name = models.CharField(max_length=80, help_text=_("Please enter your first and last name"))
    contact_position = models.CharField(max_length=80, blank=True, help_text=_("Please specify your position within your company"))
    contact_mail = models.EmailField(max_length=80)

    # base data
    scope = models.CharField(max_length=30, choices=CONTRACT_SCOPE, default=_('Service Contract'), help_text=_("Please select one suitable option"), verbose_name=_("Desired Scope"))
    wind_farm_name = models.CharField(max_length=80, help_text=_("If multiple names exists, please provide them all"))
    street_nr = models.CharField(max_length=50, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=80, blank=True, help_text=_("Please specify the city where the wind farm is located"))
    location_details = models.CharField(max_length=200, blank=True, help_text=_("You can provide additional information"))
    amount_wec = models.IntegerField(null=True, help_text=_("Please provide the number of concerned turbines"))

    #contractual partner data
    contractual_partner = models.CharField(max_length=50, blank=True)
    cp_street_nr = models.CharField(max_length=50, blank=True)
    cp_postal_code = models.CharField(max_length=20, blank=True)
    cp_city = models.CharField(max_length=80, blank=True)
    cp_contact_person = models.CharField(max_length=100, blank=True)
    cp_phone = PhoneNumberField(help_text="Format: '+49 541 38 05 38 100'", blank=True)
    cp_mail = models.EmailField(max_length=80, blank=True)
    cp_legal_form = models.CharField(max_length=50, blank=True)

    #invoice recipient
    invoice_recipient = models.CharField(max_length=50, blank=True)
    ir_street_nr = models.CharField(max_length=50, blank=True)
    ir_postal_code = models.CharField(max_length=20, blank=True)
    ir_city = models.CharField(max_length=80, blank=True)
    ir_contact_person = models.CharField(max_length=100, blank=True)
    ir_phone = PhoneNumberField(help_text="Format: '+49 541 38 05 38 100'", blank=True)
    ir_mail = models.EmailField(max_length=80, blank=True)
    ir_tax_id = models.CharField(max_length=20, blank=True)
    ir_invoice_mail = models.EmailField(max_length=80, blank=True)

    #bank data
    bank_institute = models.CharField(max_length=50, blank=True)
    iban = models.CharField(max_length=34, blank=True)
    bic = models.CharField(max_length=11, blank=True)
    vat_nr = models.CharField(max_length=50, blank=True)

    #shipping address
    sa_company = models.CharField(max_length=50, blank=True)
    sa_street_nr = models.CharField(max_length=50, blank=True)
    sa_postal_code = models.CharField(max_length=20, blank=True)
    sa_city = models.CharField(max_length=80, blank=True)
    sa_information = models.CharField(max_length=200, blank=True)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

class Turbine_CustomerQuestionnaire(models.Model):

    # base data wec
    customer_questionnaire = models.ForeignKey(CustomerQuestionnaire)
    turbine_id = models.CharField(max_length=25, blank=True, help_text=_("Please provide the Turbine ID."))
    manufacturer = models.ForeignKey('polls.Manufacturer', blank=True, null=True)
    turbine_model = models.ForeignKey('polls.WEC_Typ', blank=True, null=True, help_text=_("Enter the turbine type (e.g. V90) not the manufacturer (e.g. Vestas)!"))
    hub_height = models.DecimalField(max_digits=5, blank=True, null=True, decimal_places=1, help_text=_('Hub height in meters'))
    comissioning = models.DateField(verbose_name=_("Date of comissioning"), help_text=_('When was the WEC comissioned?'), blank=True, null=True)
    control_system = models.CharField(verbose_name=_("Control system"), max_length=30, blank=True, help_text=_('Which control system is installed?'))

    #further data
    tower_type = models.CharField(max_length=20, choices=TOWER, help_text=_("Type of tower"), default=_('Tubular Tower'), verbose_name=_("Type of tower"))
    cms = models.BooleanField(help_text=_("Is a CMS system installed?"), blank=True, default=_('No'))
    ice_sensor = models.BooleanField(help_text=_("Is an ice sensor installed?"), blank=True, default=_('No'), verbose_name=_("Ice sensor"))
    flicker_detection = models.BooleanField(help_text=_("Is a shadow-model"), blank=True, default=_('No'), verbose_name=_("Flicker detection system"))
    obstacle_light_system = models.BooleanField(help_text=_("Is a obstacle light system installed"), blank=True, default=_('No'), verbose_name=_("Obstacle light system"))

    def __str__(self):
        return str(self.id)
