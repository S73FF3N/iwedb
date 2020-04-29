# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2020-04-29 12:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0119_auto_20200429_1219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turbine_customerquestionnaire',
            name='converter_exchange',
            field=models.BooleanField(default=False, help_text='Has the converter already been replaced or overhauled? If yes, kindly check the box.'),
        ),
        migrations.AlterField(
            model_name='turbine_customerquestionnaire',
            name='gearbox_exchange',
            field=models.BooleanField(default=False, help_text='Has the gear unit already been replaced or overhauled? If yes, kindly check the box.'),
        ),
        migrations.AlterField(
            model_name='turbine_customerquestionnaire',
            name='generator_exchange',
            field=models.BooleanField(default=False, help_text='Has the generator already been replaced or overhauled? If yes, kindly check the box.'),
        ),
        migrations.AlterField(
            model_name='turbine_customerquestionnaire',
            name='rotor_blade_exchange',
            field=models.BooleanField(default=False, help_text='Have the rotor blades already been replaced or overhauled? If yes, kindly check the box.'),
        ),
    ]
