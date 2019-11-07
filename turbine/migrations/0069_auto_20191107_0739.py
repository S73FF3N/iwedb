# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-11-07 07:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('turbine', '0068_auto_20190909_1305'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicelocation',
            name='location_type',
            field=models.CharField(choices=[('External Storage', 'External Storage'), ('Engineering', 'Engineering'), ('Vehicle', 'Vehicle'), ('North-East', 'North-East'), ('North-West', 'North-West'), ('Head Quarter', 'Head Quarter'), ('South-East', 'South-East'), ('South-West', 'South-West'), ('South', 'South'), ('Middle', 'Middle'), ('Transfer Storage', 'Transfer Storage')], default='Vehicle', max_length=50),
        ),
        migrations.AlterField(
            model_name='turbine',
            name='wind_farm',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='wind_farms.WindFarm'),
        ),
    ]