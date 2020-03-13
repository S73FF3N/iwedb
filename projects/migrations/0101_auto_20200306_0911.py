# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2020-03-06 09:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0100_auto_20200306_0907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turbine_customerquestionnaire',
            name='manufacturer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.Manufacturer'),
        ),
        migrations.AlterField(
            model_name='turbine_customerquestionnaire',
            name='turbine_model',
            field=models.ForeignKey(blank=True, help_text='Enter the turbine type (e.g. V90) not the manufacturer (e.g. Vestas)!', null=True, on_delete=django.db.models.deletion.CASCADE, to='polls.WEC_Typ'),
        ),
    ]