from django.db import models
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.contrib.contenttypes import fields

from datetime import date, timedelta


EVENTS = (
    ('WKP', 'WKP'),
    ('ZOP', 'ZOP'),
    ('Getriebeendoskopie', 'Getriebeendoskopie'),
    ('Rotorblattgutachten', 'Rotorblattgutachten'),
    ('Sicherheitsüberprüfung', 'Sicherheitsüberprüfung'),
    ('BFA Wartung', 'BFA Wartung'),
    ('ZÜS BFA', 'ZÜS BFA'),
    ('Generalüberholung Winde', 'Generalüberholung Winde'),
    ('GÜ / Austausch Bordkran', 'GÜ / Austausch Bordkran'),
    ('Gittermastprüfung', 'Gittermastprüfung'),
    ('DGUV V3', 'DGUV V3'),
    )

TIME_INTERVAL = (
    ('Jahre', 'Jahre'),
    ('Monate', 'Monate'),
    ('Tage', 'Tage'),)

STATUS = (
    ('ausstehend', 'ausstehend'),
    ('eingeplant/terminiert', 'eingeplant/terminiert'),
    ('angemeldet', 'angemeldet'),
    ('durchgeführt', 'durchgeführt'),
    ('Bericht erhalten', 'Bericht erhalten'),
    ('Rechnung erhalten', 'Rechnung erhalten'),
    ('Vorgang schließen', 'Vorgang schließen'),)

PART_OF_CONTRACT = (
    ('Ja', 'Ja'),
    ('Nein', 'Nein'),
    ('zustandsorientiert', 'zustandsorientiert'),
    ('einmalig', 'einmalig'),)

class Event(models.Model):
    title = models.CharField(max_length=50, choices=EVENTS, verbose_name="Typ")
    every_count = models.PositiveIntegerField(verbose_name="Alle")
    time_interval = models.CharField(max_length=10, choices=TIME_INTERVAL, verbose_name="Zeitintervall")
    for_count = models.PositiveIntegerField(verbose_name="für")
    duration = models.CharField(max_length=10, choices=TIME_INTERVAL, verbose_name="Dauer")
    turbines = models.ManyToManyField('turbine.Turbine', related_name='event_turbines', verbose_name='WEA', db_index=True)
    done = models.DateField(verbose_name="Erste Durchführung (Soll)", default=timezone.now)
    responsible = models.ForeignKey('auth.User', help_text="Who is responsible?")

    comment = fields.GenericRelation('projects.Comment')

    def dates(self):
        dates = self.date_set.all()
        return dates

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

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('events:event_detail', args=[self.id])

class Date(models.Model):
    event = models.ForeignKey(Event, verbose_name="Gutachten")
    turbine = models.ForeignKey('turbine.Turbine', verbose_name="WEA", related_name='date_turbine')
    date = models.DateField(verbose_name="Datum (soll)", default=timezone.now)
    status = models.CharField(max_length=15, choices=STATUS)
    execution_date = models.DateField(verbose_name="Datum (ist)", null=True, blank=True)
    service_provider = models.ForeignKey('player.Player', verbose_name='Dienstleister', null=True, blank=True)
    comment = models.CharField(max_length=200, null=True, blank=True, verbose_name='Kommentar')
    part_of_contract = models.CharField(max_length=20, choices=PART_OF_CONTRACT, verbose_name='Vertragsbestandteil', null=True, blank=True)

    def _date_wind_farm_name(self):
        wind_farm = self.turbine.wind_farm.name
        return wind_farm
    date_wind_farm_name = property(_date_wind_farm_name)

    def _traffic_light(self):
        days_to_date = self.date - date.today()
        if self.status == "ausstehend" and days_to_date.days < 30:
            return 'red'
        if self.status == "geplant" and days_to_date.days < 10:
            return 'orange'
        else:
            return 'green'
    traffic_light = property(_traffic_light)