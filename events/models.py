from django.db import models
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.contrib.contenttypes import fields
from django.db.models import Max
from django.utils.translation import ugettext_lazy as _

from datetime import date, timedelta
from turbine.models import Contract


EVENTS = (
    ('Recurring inspection', _('Recurring inspection')),
    ('Condition based inspection', _('Condition based inspection')),
    ('Gearbox endoscopic inspection', _('Gearbox endoscopic inspection')),
    ('Rotor blade inspection', _('Rotor blade inspection')),
    ('Safety inspection', _('Safety inspection')),
    ('Service lift maintenance', _('Service lift maintenance')),
    ('ZÜS service lift', _('ZÜS service lift')),
    ('General Overhaul Winch', _('General Overhaul Winch')),
    ('General Overhaul Deck Crane', _('General Overhaul Deck Crane')),
    ('Lattice tower inspection', _('Lattice tower maintenance')),
    ('DGUV V3 WEC', _('DGUV V3 WEC')),
    ('DGUV V3 substation', _('DGUV V3 substation')),
    ('Maintenance of Substation', _('Maintenance of Substation')),
    ('Overcurrent Protection Inspection WEC', _('Overcurrent Protection Inspection WEC')),
    ('Overcurrent Protection Inspection Substation', _('Overcurrent Protection Inspection Substation')),
    ('UPS Battery Substation', _('UPS Battery Substation')),
    ('Inspection of pressure vessel', _('Inspection of pressure vessel')),
    ('Further official obligation', _('Further official obligation')),
    )

"""translation_dict = {
    'WKP':'Recurring inspection',
    'ZOP':'Condition based inspection',
    'Getriebeendoskopie':'Gearbox endoscopic inspection',
    'Rotorblattinspektion':'Rotor blade inspection',
    'Sicherheitsüberprüfung':'Safety inspection',
    'BFA Wartung':'Service lift maintenance',
    'ZÜS BFA':'ZÜS service lift',
    'Generalüberholung Winde':'General Overhaul Winch',
    'Generalüberholung Bordkran':'General Overhaul Deck Crane',
    'Gittermastinspektion':'Lattice tower inspection',
    'Jahre':'years',
    'Monate':'month',
    'Tage':'days',
    'ausstehend':'remaining',
    'beauftragt':'ordered',
    'angemeldet':'scheduled',
    'durchgeführt':'executed',
    'Bericht erhalten':'report received',
    'Rechnung erhalten':'invoice received',
    'abgeschlossen':'closed',
    'einmalig':'non-recurrent',
    'zustandsorientiert':'condition based',
    'ja':'yes',
    'nein':'no',
    'Vor Vertragsstart':'Before contract commencement',
    'DGUV V3 WEA':'DGUV V3 WEC',
    'DGUV V3 ÜS':'DGUV V3 substation',
    'Netzschutzprüfung WEA': 'Overcurrent Protection Inspection WEC',
    'Netzschutzprüfung ÜS': 'Overcurrent Protection Inspection Substation',
    'Wartung Übergabestation': 'Maintenance of Substation',
    'None':'None',
    'weitere behördliche Auflagen':'Further official obligation'
    }"""

TIME_INTERVAL = (
    ('years', _('years')),
    ('month', _('month')),
    ('days', _('days')),)

STATUS = (
    ('remaining', _('remaining')),
    ('ordered', _('ordered')),
    ('confirmed', _('confirmed')),
    ('scheduled', _('scheduled')),
    ('executed', _('executed')),
    ('report received', _('report received')),
    ('invoice received', _('invoice received')),
    ('closed', _('closed')),)

PART_OF_CONTRACT = (
    ('yes', _('yes')),
    ('no', _('no')),
    ('condition based', _('condition based')),
    ('non-recurrent', _('non-recurrent')),)

class Event(models.Model):
    title = models.CharField(max_length=50, choices=EVENTS, verbose_name=_("Type"))
    every_count = models.PositiveIntegerField(verbose_name=_("Every"))
    time_interval = models.CharField(max_length=10, choices=TIME_INTERVAL, verbose_name=_("Time interval"))
    for_count = models.PositiveIntegerField(verbose_name=_("for"))
    duration = models.CharField(max_length=10, choices=TIME_INTERVAL, verbose_name=_("Duration"))
    turbines = models.ManyToManyField('turbine.Turbine', related_name='event_turbines', verbose_name=_('Turbines'), db_index=True)
    done = models.DateField(verbose_name=_("Scheduled first execution"), default=timezone.now)
    part_of_contract = models.CharField(max_length=20, choices=PART_OF_CONTRACT, verbose_name=_('Part of Contract'), null=True, blank=True)
    responsibles = models.ManyToManyField('auth.User', verbose_name=_("Responsible"), help_text=_("Who is responsible?"), related_name="responsibles_for_event")

    project = models.ForeignKey('projects.Project', blank=True, null=True)

    updated = models.DateTimeField(auto_now=True, db_index=True)

    comment = fields.GenericRelation('projects.Comment')

    class Meta:
        ordering = ('-updated',)

    def dates(self):
        dates = self.date_set.all()
        return dates

    def _dated(self):
        event_dates = Date.objects.filter(event=self)
        if not event_dates:
            return _("no")
        else:
            return _("yes")
    dated = property(_dated)

    def _event_windfarm(self):
        windfarms = {}
        turbines = self.turbines.all().select_related('wind_farm')
        for t in turbines:
            try:
                windfarms[t.wind_farm.name] = t.wind_farm.get_absolute_url()
            except:
                pass
        return windfarms
    event_windfarm = property(_event_windfarm)

    def _event_windfarm_name(self):
        windfarms = self.event_windfarm
        windfarm_name = list(set([x for x in windfarms.keys()]))
        return ", ".join([str(x) for x in windfarm_name])
    event_windfarm_name = property(_event_windfarm_name)

    def _last_date(self):
        dates = Date.objects.filter(event=self)
        if dates:
            max_date = dates.aggregate(Max('date'))['date__max']
            return max_date
        else:
            return
    last_date = property(_last_date)

    def _responsible_names(self):
        responsibles = self.responsibles.all()
        return ", ".join([str(r) for r in responsibles])
    responsible_names = property(_responsible_names)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('events:event_detail', args=[str(self.id)])

class Date(models.Model):
    event = models.ForeignKey(Event, verbose_name=_("Expert Report"))
    turbine = models.ForeignKey('turbine.Turbine', verbose_name=_("Turbine"), related_name='date_turbine')
    date = models.DateField(verbose_name=_("Scheduled Date"), default=timezone.now)
    status = models.CharField(max_length=25, choices=STATUS)
    execution_date = models.DateField(verbose_name=_("Execution Date"), null=True, blank=True)
    service_provider = models.ForeignKey('player.Player', verbose_name=_('Service Provider'), null=True, blank=True)
    comment = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('Comment'))
    order_date = models.DateField(verbose_name=_("Order Date"), null=True, blank=True)

    def _date_wind_farm_name(self):
        wind_farm = self.turbine.wind_farm.name
        return wind_farm
    date_wind_farm_name = property(_date_wind_farm_name)

    def _traffic_light(self):
        if self.date <= date.today() and self.status in ["remaining", "ordered", 'confirmed', "scheduled"]:
            return 'red'
        if self.date.month == date.today().month and self.date.year == date.today().year and self.status in ["remaining", "ordered", 'confirmed', "scheduled"]:
            return 'red'
        else:
            days_to_date = self.date - date.today()
            if self.status == "remaining":
                if days_to_date.days < 180:
                    return 'orange'
                elif days_to_date.days < 90:
                    return 'red'
                else:
                    return 'white'
            elif self.status in "ordered":
                if days_to_date.days < 60:
                    return 'orange'
                elif days_to_date.days < 30:
                    return 'red'
                else:
                    return 'white'
            elif self.status in "scheduled":
                if days_to_date.days < 14:
                    return 'orange'
                else:
                    return 'white'
            else:
                return 'green'
    traffic_light = property(_traffic_light)

    def calculate_next_dates_based_on_execution_date(self):
        dates = Date.objects.filter(event=self.event, turbine=self.turbine, date__gt=self.date)
        loop_counter = 1
        if self.event.time_interval == "years":
            for d in dates:
                d.date = self.execution_date + timedelta(self.event.every_count*365*loop_counter)
                d.save()
                loop_counter += 1
        elif self.event.time_interval == "month":
            for d in dates:
                d.date = self.execution_date + timedelta(self.event.every_count*31*loop_counter)
                d.save()
                loop_counter += 1
        elif self.event.time_interval == "days":
            for d in dates:
                d.date = self.execution_date + timedelta(self.event.every_count*loop_counter)
                d.save()
                loop_counter += 1
        return

    def _contract_scope(self):
        contracts = Contract.objects.filter(active=True, turbines=self.turbine)
        if len(contracts) == 0:
            return _("not found")
        elif len(contracts) == 1:
            return contracts[0].contract_scope
        else:
            return _("multiple contracts")
    contract_scope = property(_contract_scope)

    def _responsible(self):
        responsibles = self.event.responsibles.all()
        return ", ".join([str(r) for r in responsibles])
    responsible = property(_responsible)

    def _turbine_commissioning(self):
        return self.turbine.commisioning_date()["date"]
    turbine_commissioning = property(_turbine_commissioning)

    def __str__(self):
        return self.event.get_title_display() + " | " + self.turbine.turbine_id + " | " + str(self.date.strftime('%d.%m.%Y'))




