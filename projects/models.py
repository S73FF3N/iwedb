from django.db import models
from django.db.models import Min, Case, When, Sum
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields
#from django.conf import settings

from datetime import datetime
from math import sin, cos, sqrt, atan2, radians

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
    ('DWTSW', 'DWTSW'),
    ('DWTDK', 'DWTDK'),)

DEPARTMENT = (
    ('Service', 'Service'),
    ('Technical Operations', 'Technical Operations'),)

NEW_CUSTOMER = (
    ('Yes', 'Yes'),
    ('No', 'No'),)

class Comment(models.Model):

    text = models.TextField(blank=True)
    file = models.FileField(upload_to='project_files/%Y/%m/%d/', blank=True)
    available = models.BooleanField(default=True)

    limit = models.Q(app_label = 'projects', model = 'project') | models.Q(app_label = 'player', model = 'player') | models.Q(app_label = 'player', model = 'person') | models.Q(app_label = 'polls', model = 'wec_typ') | models.Q(app_label = 'wind_farms', model = 'windfarm') | models.Q(app_label = 'turbine', model = 'turbine') | models.Q(app_label = 'turbine', model = 'contract')
    content_type = models.ForeignKey(ContentType, limit_choices_to = limit, null=True, blank=True,)
    object_id = models.PositiveIntegerField(null=True,)
    content_object = fields.GenericForeignKey('content_type', 'object_id')

    created = models.DateField(auto_now_add=True, db_index=True)
    created_by = models.ForeignKey('auth.User', default=7)#settings.AUTH_USER_MODEL

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.text

class Technologieverantwortlicher(models.Model):

    manufacturer = models.ForeignKey('polls.Manufacturer', related_name='technology')
    technology_responsible = models.ForeignKey('auth.User')

class ProjectSet(models.QuerySet):
    def add_first_commisioning(self):
        return self.annotate(first_com_date=Case(When(turbines__commisioning_year__isnull=False, then=Min('turbines__commisioning_year'))))

    def add_mw(self):
        return self.annotate(project_mw=Sum('turbines__wec_typ__output_power'))

class Project(models.Model):
    objects = ProjectSet.as_manager()

    name = models.CharField(max_length=50, db_index=True)
    slug = models.SlugField(max_length=50, db_index=True)

    offer_nr = models.CharField(max_length=50, blank=True, null=True, help_text="Offer Number (online valid for DWTS)")

    status = models.CharField(max_length=25, choices=STATUS, default='Coffee')
    prob = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Probability [%]', help_text="Estimate the probability of conclusion")
    dwt = models.CharField(max_length=30, choices=DWT, default='DWTX', help_text="Which unit is responsible for the service for this project?")
    turbines = models.ManyToManyField('turbine.Turbine', related_name='project_turbines', verbose_name='Turbines', db_index=True, help_text="Assign all turbines related to this project")
    customer = models.ForeignKey('player.Player', related_name='project_customer', help_text="Which company are we in touch with?")
    customer_contact = models.ForeignKey('player.Person', blank=True, null=True, related_name='customer_contact_projects', help_text="Who is the customer's contact person?")

    contract = models.CharField(max_length=30, choices=CONTRACT, default='New Contract')
    contract_type = models.CharField(max_length=30, choices=CONTRACT_TYPE, default='Contract Overview')
    run_time = models.IntegerField(blank=True, null=True, verbose_name='Runtime [years]')
    sales_manager = models.ForeignKey('auth.User', related_name='sales_manager', help_text="Who is the responsible Sales Manager?")
    request_date = models.DateField(default=timezone.now, blank=True, null=True, help_text="When was the first contact established?")
    start_operation = models.DateField(blank=True, null=True, help_text=" What is the intended contract commencement date?")
    contract_signature = models.DateField(blank=True, null=True, help_text="When is the contract intended to be signed?")
    price = models.IntegerField(blank=True, null=True, verbose_name='Price', help_text="State the average yearly remuneration per WTG")
    ebt = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True, verbose_name='EBT [%]', help_text="Which margin results from the price?")

    comment = fields.GenericRelation(Comment, related_query_name='comments')
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, db_index=True)
    changed_by = models.ForeignKey('auth.User', default=7)#settings.AUTH_USER_MODEL

    class Meta:
        ordering = ('-updated',)
        index_together = (('id', 'slug'),)
        permissions = (("has_sales_status", "Can create and edit Sales projects."),)

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
        last_comment = self.comment.first().created
        if last_comment <= self.updated.date():
            last_updated = last_comment.strftime('%d %b %Y')
        else:
            last_updated = self.updated.date().strftime('%d %b %Y')
        return last_updated
    last_update = property(_last_update)

    def _mw(self):
        mw = Project.objects.add_mw().get(pk=self.pk).project_mw*0.001
        return round(mw, 2)
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
        turbines = self.turbines.all()
        for t in turbines:
            try:
                windfarms[t.wind_farm.name] = t.wind_farm.get_absolute_url()
            except:
                pass
        return windfarms
    project_windfarm = property(_project_windfarm)

    def project_postal_code(self):
        postal_codes = []
        turbines = self.turbines.all()
        for t in turbines:
            if t.wind_farm.postal_code not in postal_codes:
                postal_codes.append(t.wind_farm.postal_code)
        return postal_codes

    def project_tbf(self):
        tbfs = []
        turbines = self.turbines.all()
        for t in turbines:
            tbf = t.tec_operator.all()
            for op in tbf:
                if op not in tbfs:
                    tbfs.append(op)
        return tbfs

    def _project_wec_types(self):
        turbines = self.turbines.all()
        models = {}
        for t in turbines:
            if t.wec_typ.__str__ not in models.keys():
                models[t.wec_typ.__str__] = t.wec_typ.get_absolute_url()
        return models
    project_wec_types = property(_project_wec_types)

    def _project_wec_types_name(self):
        turbines = self.turbines.all()
        models = list(set([str(x.wec_typ.name) for x in turbines]))
        if len(models) == 1:
            return models[0]
        else:
            return ", ".join([str(x) for x in models])
    project_wec_types_name = property(_project_wec_types_name)

    def _project_oem_name(self):
        turbines = self.turbines.all()
        oems = list(set([str(x.wec_typ.manufacturer.name) for x in turbines]))
        if len(oems) == 1:
            return oems[0]
        else:
            return ", ".join([str(x) for x in oems])
    project_oem_name = property(_project_oem_name)

    def _project_country(self):
        turbines = self.turbines.all()
        countries = list(set([str(x.wind_farm.country.name) for x in turbines]))
        if len(countries) == 1:
            return countries[0]
        else:
            return ", ".join([str(x) for x in countries])
    project_country = property(_project_country)

    def _project_owner(self):
        turbines = self.turbines.all()
        owners = {t.owner.name : t.owner.get_absolute_url() for t in turbines}
        return owners
    project_owner = property(_project_owner)

    def _project_owner_name(self):
        turbines = self.turbines.all()
        owners = list(set([str(x.owner.name) for x in turbines if x.owner != None]))
        if len(owners) == 1:
            return owners[0]
        else:
            return ", ".join([str(x) for x in owners])
    project_owner_name = property(_project_owner_name)

    def _project_coordinates(self):
        longitude = self.turbines.all()[0].wind_farm.longitude
        latitude = self.turbines.all()[0].wind_farm.latitude
        return {'latitude': latitude, 'longitude': longitude}
    project_coordinates = property(_project_coordinates)

    def _closest_service_location(self):
        R = 6373.0
        lat = radians(self.turbines.all()[0].wind_farm.latitude)
        lon = radians(self.turbines.all()[0].wind_farm.longitude)
        min_distance = 1000
        service_location = {'name': "non existent", 'distance': min_distance, 'postal_code': "49086"}
        service_stations = turbine.models.ServiceLocation.objects.filter(dwt=self.dwt)
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
        gas = distance * 2 * 0.3
        personnel = minutes/60.0 * 2 * 2 * 58
        costs = gas + personnel
        result = {'weekday': "{0:.2f}".format(round(costs,2)), 'saturday': "{0:.2f}".format(round(costs*1.5,2)), 'sunday': "{0:.2f}".format(round(costs*2,2))}
        return result

    def contracts_in_100km_distance(self, distance):
        R = 6373.0
        lat = radians(self.turbines.all()[0].wind_farm.latitude)
        lon = radians(self.turbines.all()[0].wind_farm.longitude)
        close_contracts = {}
        contracts = turbine.models.Contract.objects.filter(active=True)
        for contract in contracts:
            dlon = radians(contract.turbines.all()[0].wind_farm.longitude) - lon
            dlat = radians(contract.turbines.all()[0].wind_farm.latitude) - lat
            a = sin(dlat / 2)**2 + cos(lat) * cos(radians(contract.turbines.all()[0].wind_farm.latitude)) * sin(dlon / 2)**2
            b = 2 * atan2(sqrt(a), sqrt(1 - a))
            distance_c = R * b
            if distance_c < distance:
                close_contracts[contract.turbines.all()[0].wind_farm.name] = {'distance': "{0:.2f}".format(round(distance_c,2)), 'url': contract.get_absolute_url()}
            else:
                pass
        return close_contracts

    def _technologieverantwortlicher(self):
        oem_id = list(set([str(x.wec_typ.manufacturer.id) for x in self.turbines.all()]))#self.turbines.all().order_by().values_list("wec_typ__manufacturer__id", flat=True).distinct()
        technology_responsible = []
        for m in oem_id:
            p = Technologieverantwortlicher.objects.get(manufacturer__id=m)
            technology_responsible.append(p.technology_responsible.__str__())
        return ", ".join(technology_responsible)
    technologieverantwortlicher = property(_technologieverantwortlicher)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('projects:project_detail', args=[self.id, self.slug])

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
