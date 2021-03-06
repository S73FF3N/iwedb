# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-08-28 07:33
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('wind_farms', '0040_auto_20170828_0715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 8, 28, 7, 33, 19, 719729, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='contract',
            name='start_date',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 8, 28, 7, 33, 19, 719666, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='windfarm',
            name='commisioning',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 8, 28, 7, 33, 19, 711243, tzinfo=utc), null=True, verbose_name='Commisioning date'),
        ),
        migrations.AlterField(
            model_name='windfarm',
            name='dismantling',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 8, 28, 7, 33, 19, 711324, tzinfo=utc), null=True),
        ),
    ]
