# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-08-02 06:59
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('wind_farms', '0019_auto_20170802_0626'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='windfarm',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='windfarm',
            name='longitude',
        ),
        migrations.AlterField(
            model_name='windfarm',
            name='commisioning',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 8, 2, 6, 59, 4, 161817, tzinfo=utc), null=True, verbose_name='Commisioning date'),
        ),
        migrations.AlterField(
            model_name='windfarm',
            name='dismantling',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 8, 2, 6, 59, 4, 161873, tzinfo=utc), null=True),
        ),
    ]