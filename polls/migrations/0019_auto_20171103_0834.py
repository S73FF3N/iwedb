# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-11-03 08:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0018_auto_20171028_1159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wec_typ',
            name='hub_weight_t',
            field=models.DecimalField(blank=True, decimal_places=2, default=100, max_digits=5, null=True, verbose_name='Nacelle weight [t]'),
        ),
        migrations.AlterField(
            model_name='wec_typ',
            name='max_hub_height',
            field=models.DecimalField(blank=True, decimal_places=2, default=140, max_digits=5, null=True, verbose_name='Max. Hub Height'),
        ),
        migrations.AlterField(
            model_name='wec_typ',
            name='min_hub_height',
            field=models.DecimalField(blank=True, decimal_places=2, default=60, max_digits=5, null=True, verbose_name='Min. Hub Height'),
        ),
        migrations.AlterField(
            model_name='wec_typ',
            name='output_power',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Output power [kW]'),
        ),
        migrations.AlterField(
            model_name='wec_typ',
            name='rotor_weight_t',
            field=models.DecimalField(blank=True, decimal_places=2, default=50, max_digits=5, null=True, verbose_name='Rotor weight [t]'),
        ),
        migrations.AlterField(
            model_name='wec_typ',
            name='tot_weight_t',
            field=models.DecimalField(blank=True, decimal_places=2, default=400, max_digits=5, null=True, verbose_name='Total weight [t]'),
        ),
        migrations.AlterField(
            model_name='wec_typ',
            name='tower_weight_t',
            field=models.DecimalField(blank=True, decimal_places=2, default=250, max_digits=5, null=True, verbose_name='Tower weight [t]'),
        ),
    ]
