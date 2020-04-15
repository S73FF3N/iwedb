from django.db import models
from django.core.urlresolvers import reverse
from django.db.models import Min, Case, When
from django.contrib.contenttypes import fields
from django.utils.translation import ugettext_lazy as _

import polls

class Country(models.Model):
    name = models.CharField(max_length=200, db_index=True)

    def __str__(self):
        return self.name

class WindFarmSet(models.QuerySet):
    def add_first_commisioning(self):
        return self.annotate(first_com_date=Case(When(turbine__commisioning__isnull=False, then=Min('turbine__commisioning'))))

class WindFarm(models.Model):

    name = models.CharField(max_length=80, db_index=True, help_text=_("Avoid wind farm names like: 'Hörup II', 'Hörup repowering' or 'Hörup extension'"))
    second_name = models.CharField(max_length=80, blank=True, help_text=_("In case a second name for the wind farm is known, please provide it."), verbose_name=_("Second Name"))
    slug = models.SlugField(max_length=200, db_index=True)
    description = models.TextField(blank=True, help_text=_("Additional information like: Is composed of two parts"), verbose_name=_("Description"))
    country = models.ForeignKey(Country, related_name='countries', default=67, verbose_name=_("Country"))
    postal_code = models.CharField(max_length=20, blank=True, verbose_name=_("Postal Code"))
    city = models.CharField(max_length=80, blank=True, help_text=_("Please specify ONE city"), verbose_name=_("City"))
    offshore = models.BooleanField(default=False, help_text=_("Is the wind farm built offshore?"))
    latitude = models.FloatField(blank=True, null=True, help_text=_("Enter an approximation of the wind farm's centre"))
    longitude = models.FloatField(blank=True, null=True, help_text=_("Enter an approximation of the wind farm's centre"))
    comment = fields.GenericRelation('projects.Comment', verbose_name=_("Comment"))
    available = models.BooleanField(default=True, verbose_name=_("Available"))
    created = models.DateField(auto_now_add=True, verbose_name=_("Created"))
    updated = models.DateField(auto_now=True, verbose_name=_("Updated"))

    objects = WindFarmSet.as_manager()

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def turbines(self):
        WF_turbines = self.turbine_set.all()
        return WF_turbines

    def _amount_turbines(self):
        WF_turbines = self.turbine_set
        return WF_turbines.count()
    amount_turbines = property(_amount_turbines)

    def get_turbines_in_production(self):
        WF_turbines = self.turbine_set.filter(status="in production")
        return WF_turbines

    def _amount_turbines_in_production(self):
        WF_turbines = self.turbine_set.filter(status="in production")
        return WF_turbines.count()
    amount_turbines_in_production = property(_amount_turbines_in_production)

    def get_turbines_dismantled(self):
        WF_turbines = self.turbine_set.filter(status="dismantled")
        return WF_turbines

    def get_turbines_planned(self):
        planned = self.turbine_set.filter(status="planned")
        return planned

    def get_turbines_construction(self):
        construction = self.turbine_set.filter(status="under construction")
        return construction

    def _get_first_commisioning(self):
        first_commisioning = self.first_com_date
        return first_commisioning
    get_first_commisioning = property(_get_first_commisioning)

    def get_offshore_status(self):
        if self.offshore == True:
            return _('Yes')
        else:
            return _('No')

    def get_status(self):
        production = self.turbine_set.filter(status="in production")
        planned = self.turbine_set.filter(status="planned")
        construction = self.turbine_set.filter(status="under construction")
        dismantled = self.turbine_set.filter(status="dismantled")
        if production.exists():
            return _('in production')
        elif planned.exists() or construction.exists():
            return _('planned/under construction')
        elif dismantled.exists():
            return _('dismantled')
        else:
            return _('no turbines assigned')

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

    def _wind_farm_wec_types_name(self):
        wec_types = self.turbine_set.all().select_related('wec_typ', 'wec_typ__manufacturer').order_by().values_list('wec_typ', flat=True).distinct()
        models = polls.models.WEC_Typ.objects.filter(id__in=wec_types).select_related('manufacturer').values_list('manufacturer__name', 'name')
        return ", ".join([" ".join(map(str,x)) for x in models])
    wind_farm_wec_types_name = property(_wind_farm_wec_types_name)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('wind_farms:windfarm_detail', args=[self.id, self.slug])
