# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-07-13 13:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20170713_0800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wec_typ',
            name='cut_in',
            field=models.DecimalField(blank=True, decimal_places=2, default=3.5, max_digits=5),
        ),
        migrations.AlterField(
            model_name='wec_typ',
            name='cut_out',
            field=models.DecimalField(blank=True, decimal_places=2, default=25.0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='wec_typ',
            name='drive',
            field=models.CharField(choices=[('gearbox', 'GEA'), ('gearless', 'NOG')], default='GEA', max_length=20),
        ),
        migrations.AlterField(
            model_name='wec_typ',
            name='hub_weight_t',
            field=models.IntegerField(blank=True, default=100),
        ),
        migrations.AlterField(
            model_name='wec_typ',
            name='image',
            field=models.ImageField(blank=True, upload_to='wec_types/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='wec_typ',
            name='max_hub_height',
            field=models.IntegerField(blank=True, default=140),
        ),
        migrations.AlterField(
            model_name='wec_typ',
            name='max_rot_speed_r_m',
            field=models.DecimalField(blank=True, decimal_places=2, default=20.5, max_digits=5),
        ),
        migrations.AlterField(
            model_name='wec_typ',
            name='min_hub_height',
            field=models.IntegerField(blank=True, default=60),
        ),
        migrations.AlterField(
            model_name='wec_typ',
            name='min_rot_speed_r_m',
            field=models.DecimalField(blank=True, decimal_places=2, default=11.5, max_digits=5),
        ),
        migrations.AlterField(
            model_name='wec_typ',
            name='nominal_speed',
            field=models.DecimalField(blank=True, decimal_places=2, default=15.0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='wec_typ',
            name='offshore',
            field=models.CharField(choices=[('yes', 'YES'), ('no', 'NO')], default='NO', max_length=20),
        ),
        migrations.AlterField(
            model_name='wec_typ',
            name='output_power',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='wec_typ',
            name='reg',
            field=models.CharField(choices=[('pitch', 'PIT'), ('stall', 'STA')], default='PIT', max_length=20),
        ),
        migrations.AlterField(
            model_name='wec_typ',
            name='rotor_diameter',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='wec_typ',
            name='rotor_weight_t',
            field=models.IntegerField(blank=True, default=50),
        ),
        migrations.AlterField(
            model_name='wec_typ',
            name='tot_weight_t',
            field=models.IntegerField(blank=True, default=400),
        ),
        migrations.AlterField(
            model_name='wec_typ',
            name='tower_weight_t',
            field=models.IntegerField(blank=True, default=250),
        ),
        migrations.AlterField(
            model_name='wec_typ',
            name='wind_class',
            field=models.CharField(blank=True, default='IEC Ia', max_length=200),
        ),
        migrations.AlterField(
            model_name='wec_typ',
            name='year',
            field=models.IntegerField(blank=True, default=2000),
        ),
    ]
