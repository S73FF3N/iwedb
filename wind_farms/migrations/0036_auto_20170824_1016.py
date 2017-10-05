# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-08-24 10:16
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('wind_farms', '0035_auto_20170824_0851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 8, 24, 10, 16, 30, 659168, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='contract',
            name='start_date',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 8, 24, 10, 16, 30, 659128, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='windfarm',
            name='commisioning',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 8, 24, 10, 16, 30, 654808, tzinfo=utc), null=True, verbose_name='Commisioning date'),
        ),
        migrations.AlterField(
            model_name='windfarm',
            name='dismantling',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 8, 24, 10, 16, 30, 654852, tzinfo=utc), null=True),
        ),
    ]
