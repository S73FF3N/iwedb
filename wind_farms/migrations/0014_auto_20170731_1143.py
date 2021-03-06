# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-07-31 11:43
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('wind_farms', '0013_auto_20170728_1954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='windfarm',
            name='commisioning',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 7, 31, 11, 43, 13, 691441, tzinfo=utc), null=True, verbose_name='Commisioning date'),
        ),
        migrations.AlterField(
            model_name='windfarm',
            name='dismantling',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 7, 31, 11, 43, 13, 691489, tzinfo=utc), null=True),
        ),
    ]
