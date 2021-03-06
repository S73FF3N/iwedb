# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2020-01-17 11:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0021_event_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='done',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Scheduled first execution'),
        ),
        migrations.AlterField(
            model_name='event',
            name='duration',
            field=models.CharField(choices=[('Jahre', 'Jahre'), ('Monate', 'Monate'), ('Tage', 'Tage')], max_length=10, verbose_name='Duration'),
        ),
        migrations.AlterField(
            model_name='event',
            name='every_count',
            field=models.PositiveIntegerField(verbose_name='Every'),
        ),
        migrations.AlterField(
            model_name='event',
            name='for_count',
            field=models.PositiveIntegerField(verbose_name='for'),
        ),
        migrations.AlterField(
            model_name='event',
            name='time_interval',
            field=models.CharField(choices=[('Jahre', 'Jahre'), ('Monate', 'Monate'), ('Tage', 'Tage')], max_length=10, verbose_name='Time interval'),
        ),
        migrations.AlterField(
            model_name='event',
            name='title',
            field=models.CharField(choices=[('WKP', 'WKP'), ('ZOP', 'ZOP'), ('Getriebeendoskopie', 'Getriebeendoskopie'), ('Rotorblattgutachten', 'Rotorblattgutachten'), ('Sicherheitsüberprüfung', 'Sicherheitsüberprüfung'), ('BFA Wartung', 'BFA Wartung'), ('ZÜS BFA', 'ZÜS BFA'), ('Generalüberholung Winde', 'Generalüberholung Winde'), ('GÜ / Austausch Bordkran', 'GÜ / Austausch Bordkran'), ('Gittermastprüfung', 'Gittermastprüfung'), ('DGUV V3', 'DGUV V3')], max_length=50, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='event',
            name='turbines',
            field=models.ManyToManyField(db_index=True, related_name='event_turbines', to='turbine.Turbine', verbose_name='Turbines'),
        ),
    ]
