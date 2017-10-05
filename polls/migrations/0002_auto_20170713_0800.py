# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-13 08:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='wec_typ',
            name='cut_in',
            field=models.DecimalField(decimal_places=2, default=3.5, max_digits=5),
        ),
        migrations.AddField(
            model_name='wec_typ',
            name='cut_out',
            field=models.DecimalField(decimal_places=2, default=25.0, max_digits=5),
        ),
        migrations.AddField(
            model_name='wec_typ',
            name='drive',
            field=models.CharField(choices=[(b'GEA', b'gearbox'), (b'NOG', b'gearless')], default=b'gearbox', max_length=3),
        ),
        migrations.AddField(
            model_name='wec_typ',
            name='hub_weight_t',
            field=models.IntegerField(default=100),
        ),
        migrations.AddField(
            model_name='wec_typ',
            name='max_hub_height',
            field=models.IntegerField(default=140),
        ),
        migrations.AddField(
            model_name='wec_typ',
            name='max_rot_speed_r_m',
            field=models.DecimalField(decimal_places=2, default=20.5, max_digits=5),
        ),
        migrations.AddField(
            model_name='wec_typ',
            name='min_hub_height',
            field=models.IntegerField(default=60),
        ),
        migrations.AddField(
            model_name='wec_typ',
            name='min_rot_speed_r_m',
            field=models.DecimalField(decimal_places=2, default=11.5, max_digits=5),
        ),
        migrations.AddField(
            model_name='wec_typ',
            name='nominal_speed',
            field=models.DecimalField(decimal_places=2, default=15.0, max_digits=5),
        ),
        migrations.AddField(
            model_name='wec_typ',
            name='offshore',
            field=models.CharField(choices=[(b'YES', b'yes'), (b'NO', b'no')], default=b'yes', max_length=3),
        ),
        migrations.AddField(
            model_name='wec_typ',
            name='reg',
            field=models.CharField(choices=[(b'PIT', b'pitch'), (b'STA', b'stall')], default=b'pitch', max_length=3),
        ),
        migrations.AddField(
            model_name='wec_typ',
            name='rotor_diameter',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='wec_typ',
            name='rotor_weight_t',
            field=models.IntegerField(default=50),
        ),
        migrations.AddField(
            model_name='wec_typ',
            name='tot_weight_t',
            field=models.IntegerField(default=400),
        ),
        migrations.AddField(
            model_name='wec_typ',
            name='tower_weight_t',
            field=models.IntegerField(default=250),
        ),
        migrations.AddField(
            model_name='wec_typ',
            name='wind_class',
            field=models.CharField(default=b'IEC Ia', max_length=200),
        ),
        migrations.AddField(
            model_name='wec_typ',
            name='year',
            field=models.IntegerField(default=2000),
        ),
    ]
