from django.db import models
from django.core.urlresolvers import reverse
from django.db.models import Min

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

class Country(models.Model):
    name = models.CharField(max_length=200, db_index=True)

    def __str__(self):
        return self.name

class WindFarm(models.Model):

    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    description = models.TextField(blank=True, null=True)
    country = models.ForeignKey(Country, related_name='countries')
    city = models.CharField(max_length=200, blank=True, null=True)
    #commisioning = models.DateField(blank=True, null=True, verbose_name='Commisioning date', default=timezone.now)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    available = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def turbines(self):
        WF_turbines = self.turbine_set.all()
        return WF_turbines

    def get_turbines_in_farm(self):
        WF_turbines = self.turbine_set.all()
        return len(WF_turbines)

    def get_first_commisioning(self):
        sorted_by_commisioning = self.turbine_set.all().aggregate(first=Min('commisioning'))['first']
        return sorted_by_commisioning

    #def get_turbine_amount_by_model(self):
    #    dict = {}
    #    turbine_amount_by_model = []
    #    for i in self.objects.filter(available=True):
    #        dict[i.wec_type.name] += i.amount_turbines
    #    for k, v in dict:
    #        turbine_amount_by_model.append([k,v])
    #    turbine_amount_by_model.set(0, ["Model", "Amount of turbines"])
    #    return turbine_amount_by_model

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('wind_farms:windfarm_detail', args=[self.id, self.slug])
