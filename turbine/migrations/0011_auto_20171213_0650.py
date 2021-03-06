# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-12-13 06:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('turbine', '0010_auto_20171128_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turbine',
            name='turbine_id',
            field=models.CharField(db_index=True, max_length=25),
        ),
        migrations.AlterField(
            model_name='turbine',
            name='wec_manufacturer',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='wec_manufacturers', to='polls.Manufacturer', verbose_name='Manufacturer'),
        ),
        migrations.AlterField(
            model_name='turbine',
            name='wec_typ',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='polls.WEC_Typ', verbose_name='Model'),
        ),
    ]
