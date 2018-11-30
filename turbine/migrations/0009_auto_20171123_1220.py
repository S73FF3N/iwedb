# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-11-23 12:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('turbine', '0008_auto_20171121_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turbine',
            name='wind_farm',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wind_farms.WindFarm'),
        ),
    ]