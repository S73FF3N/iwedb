# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-08-16 08:35
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('wind_farms', '0028_auto_20170816_0832'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='windfarm',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='wind_farms.WindFarm'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contract',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 8, 16, 8, 35, 39, 865649, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='contract',
            name='start_date',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 8, 16, 8, 35, 39, 865591, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='windfarm',
            name='commisioning',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 8, 16, 8, 35, 39, 859654, tzinfo=utc), null=True, verbose_name='Commisioning date'),
        ),
        migrations.AlterField(
            model_name='windfarm',
            name='dismantling',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 8, 16, 8, 35, 39, 859732, tzinfo=utc), null=True),
        ),
    ]
