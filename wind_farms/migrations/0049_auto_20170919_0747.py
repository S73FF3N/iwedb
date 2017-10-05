# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-09-19 07:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wind_farms', '0048_auto_20170911_1039'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contract',
            name='actor',
        ),
        migrations.RemoveField(
            model_name='contract',
            name='windfarm',
        ),
        migrations.RemoveField(
            model_name='windfarm',
            name='amount_turbines',
        ),
        migrations.RemoveField(
            model_name='windfarm',
            name='com_operator',
        ),
        migrations.RemoveField(
            model_name='windfarm',
            name='commisioning',
        ),
        migrations.RemoveField(
            model_name='windfarm',
            name='developer',
        ),
        migrations.RemoveField(
            model_name='windfarm',
            name='dismantling',
        ),
        migrations.RemoveField(
            model_name='windfarm',
            name='follow_up_farm',
        ),
        migrations.RemoveField(
            model_name='windfarm',
            name='hub_height',
        ),
        migrations.RemoveField(
            model_name='windfarm',
            name='manufacturer',
        ),
        migrations.RemoveField(
            model_name='windfarm',
            name='offshore',
        ),
        migrations.RemoveField(
            model_name='windfarm',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='windfarm',
            name='repowered',
        ),
        migrations.RemoveField(
            model_name='windfarm',
            name='service',
        ),
        migrations.RemoveField(
            model_name='windfarm',
            name='status',
        ),
        migrations.RemoveField(
            model_name='windfarm',
            name='tec_operator',
        ),
        migrations.RemoveField(
            model_name='windfarm',
            name='wec_typ',
        ),
        migrations.DeleteModel(
            name='Contract',
        ),
    ]
