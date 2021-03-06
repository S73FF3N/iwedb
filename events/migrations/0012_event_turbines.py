# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-10-14 07:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turbine', '0068_auto_20190909_1305'),
        ('events', '0011_auto_20191008_0907'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='turbines',
            field=models.ManyToManyField(db_index=True, related_name='event_turbines', to='turbine.Turbine', verbose_name='WEA'),
        ),
    ]
