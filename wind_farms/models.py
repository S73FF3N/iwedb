from django.db import models
from django.core.urlresolvers import reverse
from django.db.models import Min
from django.contrib.contenttypes import fields

import polls

class Country(models.Model):
    name = models.CharField(max_length=200, db_index=True)

    def __str__(self):
        return self.name

class WindFarm(models.Model):

    name = models.CharField(max_length=80, db_index=True, help_text="Avoid wind farm names like: 'Hörup II', 'Hörup repowering' or 'Hörup extension'")
    slug = models.SlugField(max_length=200, db_index=True)
    description = models.TextField(blank=True, help_text="Additional information like: Is composed of two parts")
    country = models.ForeignKey(Country, related_name='countries', blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=80, blank=True)
    offshore = models.BooleanField(default=False, help_text="Is the wind farm built offshore?")
    latitude = models.FloatField(help_text="Enter an approximation of the wind farm's centre", default=1.8066702)
    longitude = models.FloatField(help_text="Enter an approximation of the wind farm's centre", default=49.8046937)
    comment = fields.GenericRelation('projects.Comment')
    available = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def turbines(self):
        WF_turbines = self.turbine_set.all()
        return WF_turbines

    def amount_turbines(self):
        WF_turbines = self.turbine_set.all()
        return WF_turbines.count()

    def get_turbines_in_production(self):
        WF_turbines = self.turbine_set.all().filter(status="in production")
        return WF_turbines

    def amount_turbines_in_production(self):
        WF_turbines = self.turbine_set.all().filter(status="in production")
        return len(WF_turbines)

    def get_turbines_dismantled(self):
        WF_turbines = self.turbine_set.all().filter(status="dismantled")
        return WF_turbines

    def get_turbines_planned(self):
        planned = self.turbine_set.all().filter(status="planned")
        return planned

    def get_turbines_construction(self):
        construction = self.turbine_set.all().filter(status="under construction")
        return construction

    def get_first_commisioning(self):
        sorted_by_commisioning = self.turbine_set.all().aggregate(first=Min('commisioning'))['first']
        return sorted_by_commisioning

    def get_offshore_status(self):
        if self.offshore == True:
            return 'Yes'
        else:
            return 'No'

    def get_status(self):
        production = self.turbine_set.all().filter(status="in production")
        planned = self.turbine_set.all().filter(status="planned")
        construction = self.turbine_set.all().filter(status="under construction")
        dismantled = self.turbine_set.all().filter(status="dismantled")
        if production.exists():
            return 'in production'
        elif planned.exists() or construction.exists():
            return 'planned/under construction'
        elif dismantled.exists():
            return 'dismantled'
        else:
            return 'no turbines assigned'

    def get_distinct_wec_typ(self):
        wec_typ_count = self.turbine_set.all().values('wec_typ')
        amount_turbines = {}
        for t in wec_typ_count:
            wec_typ = polls.models.WEC_Typ.objects.get(id=t['wec_typ']).name
            manufacturer = polls.models.WEC_Typ.objects.get(id=t['wec_typ']).manufacturer
            url = polls.models.WEC_Typ.objects.get(id=t['wec_typ']).get_absolute_url
            if str(wec_typ) not in amount_turbines:
                amount_turbines[wec_typ] = [1, manufacturer, url]
            else:
                amount_turbines[wec_typ][0] += 1
        return amount_turbines

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('wind_farms:windfarm_detail', args=[self.id, self.slug])
