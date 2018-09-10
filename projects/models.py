from django.db import models
from django.db.models import Min
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields
#from django.conf import settings

from datetime import datetime
from math import sin, cos, sqrt, atan2, radians

import turbine.models

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

CONTRACT = (
    ('Basic Maintenance', 'Basic Maintenance'),
    ('Full Maintenance without MC', 'Full Maintenance without MC'),
    ('Full Maintenance with MC', 'Full Maintenance with MC'),
    ('Extension', 'Extension'),
    ('Extension without MC', 'Extension without MC'),
    ('Extension with MC', 'Extension with MC'),
    ('Spare Parts', 'Spare Parts'),
    ('Other', 'Other'),)

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
    ('Technical Operations', 'Technical Operations'),
    ('Remote Control', 'Remote Control'),)

NEW_CUSTOMER = (
    ('Yes', 'Yes'),
    ('No', 'No'),)

class Comment(models.Model):

    text = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='project_files/%Y/%m/%d/', null=True, blank=True)
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

class Project(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    slug = models.SlugField(max_length=50, db_index=True)

    status = models.CharField(max_length=25, choices=STATUS, default='Coffee')
    prob = models.DecimalField(max_digits=5, decimal_places=2, default=50, blank=True, null=True, verbose_name='Probability [%]')
    new_customer = models.CharField(max_length=30, choices=NEW_CUSTOMER, default='No')
    dwt = models.CharField(max_length=30, choices=DWT, default='DWTX')
    turbines = models.ManyToManyField('turbine.Turbine', related_name='project_turbines', verbose_name='Turbines', db_index=True)
    customer = models.ForeignKey('player.Player', related_name='project_customer')
    customer_contact = models.ForeignKey('player.Person', blank=True, null=True, related_name='customer_contact_projects')

    contract_type = models.CharField(max_length=30, choices=CONTRACT, default='Contract Overview')
    run_time = models.IntegerField(default=5, blank=True, null=True, verbose_name='Runtime [years]')
    department = models.CharField(max_length=20, choices=DEPARTMENT, default='Service')
    responsible = models.CharField(max_length=20, blank=True, null=True)
    request_date = models.DateField(default=timezone.now, blank=True, null=True)
    start_operation = models.DateField(default=timezone.now, blank=True, null=True)
    contract_signature = models.DateField(default=timezone.now, blank=True, null=True)
    price = models.IntegerField(default=35000, blank=True, null=True, verbose_name='Price [€/WTG/year]')
    ebt = models.DecimalField(default=15, max_digits=4, decimal_places=2, blank=True, null=True, verbose_name='EBT [%]')

    comment = fields.GenericRelation(Comment, related_query_name='comments')
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, db_index=True)
    changed_by = models.ForeignKey('auth.User', default=7)#settings.AUTH_USER_MODEL

    class Meta:
        ordering = ('-updated',)
        index_together = (('id', 'slug'),)
        permissions = (("has_sales_status", "Can create and edit Sales projects."),)

    def amount_turbines(self):
        project_turbines = self.turbines.all().count()
        return project_turbines

    def all_comments(self):
        comment_list = self.comment.exclude(text__in=['created project', 'edited project'])
        comment_str_list = []
        for c in comment_list:
            comment_str_list.append(': '.join([str(c.created), c.text]))
        comment_str = '; '.join(comment_str_list)
        return comment_str

    def last_update(self):
        last_comment = self.comment.first().created
        if last_comment <= self.updated.date():
            last_updated = last_comment.strftime('%d %b %Y')
        else:
            last_updated = self.updated.date().strftime('%d %b %Y')
        return last_updated

    def mw(self):
        mw = sum(self.turbines.all().order_by().values_list('wec_typ__output_power', flat=True))*0.001
        return round(mw, 2)

    def yearly_contract_value(self):
        try:
            total = self.price * self.turbines.all().count()
        except:
            total = "not defined"
        return total

    def total_contract_value(self):
        try:
            total = self.price * self.run_time * self.turbines.all().count()
        except:
            total = "not defined"
        return total

    def first_commisioning(self):
        try:
            f_c = self.turbines.all().aggregate(first=Min('commisioning'))['first']
        except:
            f_c = "not defined"
        return f_c

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

    def project_windfarm(self):
        windfarms = {}
        for t in self.turbines.all():
            try:
                windfarms[t.wind_farm.name] = t.wind_farm.get_absolute_url()
            except:
                pass
        #windfarms = {t.wind_farm.name : t.wind_farm.get_absolute_url() for t in self.turbines.all()}
        return windfarms

    def project_windfarm_name(self):
        windfarms = self.turbines.exclude(wind_farm__name__isnull=True).order_by().values_list("wind_farm__name", flat=True).distinct()
        if len(windfarms) == 1:
            return windfarms[0]
        else:
            return ", ".join([str(x) for x in windfarms])

    def project_wec_types(self):
        oem_name = self.turbines.all().order_by().values_list("wec_typ__manufacturer__name", flat=True).distinct()
        wec_typ_name = self.turbines.all().order_by().values_list("wec_typ__name", flat=True).distinct()
        models_name = []
        for i in range(len(oem_name)):
            models_name.append(" ".join([oem_name[i], wec_typ_name[i]]))
        models_link = [t.wec_typ.get_absolute_url() for t in self.turbines.all()]
        models_link = list(set(models_link))
        models = dict(zip(models_name, models_link))
        return models

    def project_wec_types_name(self):
        models = self.turbines.all().order_by().values_list("wec_typ__name", flat=True).distinct()
        if len(models) == 1:
            return models[0]
        else:
            return ", ".join([str(x) for x in models])

    def project_oem_name(self):
        oems = self.turbines.all().order_by().values_list("wec_typ__manufacturer__name", flat=True).distinct()
        if len(oems) == 1:
            return oems[0]
        else:
            return ", ".join([str(x) for x in oems])

    def project_country(self):
        countries = self.turbines.all().order_by().values_list("wind_farm__country__name", flat=True).distinct()
        if len(countries) == 1:
            return countries[0]
        else:
            return ", ".join([str(x) for x in countries])

    def project_city(self):
        cities = self.turbines.all().order_by().values_list("wind_farm__city", flat=True).distinct()
        if len(cities) == 1:
            return cities[0]
        else:
            return ", ".join([str(x) for x in cities])

    def project_postal(self):
        postals = self.turbines.all().order_by().values_list("wind_farm__postal_code", flat=True).distinct()
        if len(postals) == 1:
            return postals[0]
        else:
            return ", ".join([str(x) for x in postals])

    def project_owner(self):
        owners = {t.owner.name : t.owner.get_absolute_url() for t in self.turbines.all()}
        return owners

    def project_owner_name(self):
        owners = self.turbines.all().order_by().values_list("owner__name", flat=True).distinct()
        if len(owners) == 1:
            return owners[0]
        else:
            return ", ".join([str(x) for x in owners])

    def closest_service_location(self):
        R = 6373.0
        coord = 1
        try:
            lat = radians(self.turbines.all()[0].latitude)
            lon = radians(self.turbines.all()[0].longitude)
        except:
            try:
                lat = radians(self.turbines.all()[0].wind_farm.latitude)
                lon = radians(self.turbines.all()[0].wind_farm.longitude)
            except:
                coord = None
        if not coord == None:
            min_distance = 1000
            service_location = {'name': "non existent", 'distance': min_distance, 'postal_code': "49086"}
            for s in turbine.models.ServiceLocation.objects.filter(dwt="DWTX"):
                dlon = radians(s.longitude) - lon
                dlat = radians(s.latitude) - lat
                a = sin(dlat / 2)**2 + cos(lat) * cos(radians(s.latitude)) * sin(dlon / 2)**2
                c = 2 * atan2(sqrt(a), sqrt(1 - a))
                distance = R * c
                if distance < min_distance:
                    min_distance = distance
                    service_location = {'name': s.name, 'distance': "{0:.2f}".format(round(min_distance,2)), 'postal_code': s.postal_code}
                else:
                    pass
        else:
            service_location = "coordinates missing"
        return service_location

    def driving_rate(self, distance, minutes):
        gas = distance * 2 * 0.3
        personnel = minutes/60.0 * 2 * 2 * 58
        costs = gas + personnel
        result = {'weekday': "{0:.2f}".format(round(costs,2)), 'saturday': "{0:.2f}".format(round(costs*1.5,2)), 'sunday': "{0:.2f}".format(round(costs*2,2))}
        return result

    def contracts_in_100km_distance(self):
        R = 6373.0
        coord = 1
        try:
            lat = radians(self.turbines.all()[0].latitude)
            lon = radians(self.turbines.all()[0].longitude)
        except:
            try:
                lat = radians(self.turbines.all()[0].wind_farm.latitude)
                lon = radians(self.turbines.all()[0].wind_farm.longitude)
            except:
                coord = None
        if not coord == None:
            close_contracts = {}
            for c in turbine.models.Contract.objects.all():
                dlon = radians(c.turbines.all()[0].longitude) - lon
                dlat = radians(c.turbines.all()[0].latitude) - lat
                a = sin(dlat / 2)**2 + cos(lat) * cos(radians(c.turbines.all()[0].latitude)) * sin(dlon / 2)**2
                b = 2 * atan2(sqrt(a), sqrt(1 - a))
                distance = R * b
                if distance < 100:
                    close_contracts[c.turbines.all()[0].wind_farm.name] = {'distance': "{0:.2f}".format(round(distance,2)), 'url': c.get_absolute_url()}
                else:
                    pass
        else:
            close_contracts = "coordinates missing"
        return close_contracts

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('projects:project_detail', args=[self.id, self.slug])
