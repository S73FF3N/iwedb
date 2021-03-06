# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-12-19 10:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wind_farms', '0059_auto_20181030_0942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='windfarm',
            name='latitude',
            field=models.FloatField(blank=True, help_text="Enter an approximation of the wind farm's centre", null=True),
        ),
        migrations.AlterField(
            model_name='windfarm',
            name='longitude',
            field=models.FloatField(blank=True, help_text="Enter an approximation of the wind farm's centre", null=True),
        ),
    ]
