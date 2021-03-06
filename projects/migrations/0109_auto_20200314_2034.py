# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2020-03-14 20:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0108_auto_20200313_1503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turbine_customerquestionnaire',
            name='tower_type',
            field=models.CharField(choices=[('Lattice Tower', 'Lattice Tower'), ('Tubular Tower', 'Tubular Tower')], default='Tubular Tower', help_text='Type of tower', max_length=20, verbose_name='Type of tower'),
        ),
        migrations.AlterField(
            model_name='turbine_customerquestionnaire',
            name='tower_type_de',
            field=models.CharField(choices=[('Lattice Tower', 'Lattice Tower'), ('Tubular Tower', 'Tubular Tower')], default='Tubular Tower', help_text='Type of tower', max_length=20, null=True, verbose_name='Type of tower'),
        ),
        migrations.AlterField(
            model_name='turbine_customerquestionnaire',
            name='tower_type_en',
            field=models.CharField(choices=[('Lattice Tower', 'Lattice Tower'), ('Tubular Tower', 'Tubular Tower')], default='Tubular Tower', help_text='Type of tower', max_length=20, null=True, verbose_name='Type of tower'),
        ),
        migrations.AlterField(
            model_name='turbine_customerquestionnaire',
            name='turbine_id',
            field=models.CharField(blank=True, help_text='Please provide the Turbine ID.', max_length=25),
        ),
    ]
