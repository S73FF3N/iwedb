# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-08-01 06:49
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('wind_farms', '0016_auto_20170801_0627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='windfarm',
            name='com_operator',
            field=models.ManyToManyField(blank=True, null=True, related_name='com_operators', to='player.Player'),
        ),
        migrations.AlterField(
            model_name='windfarm',
            name='commisioning',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 8, 1, 6, 49, 22, 399693, tzinfo=utc), null=True, verbose_name='Commisioning date'),
        ),
        migrations.AlterField(
            model_name='windfarm',
            name='developer',
            field=models.ManyToManyField(blank=True, null=True, related_name='developers', to='player.Player'),
        ),
        migrations.AlterField(
            model_name='windfarm',
            name='dismantling',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 8, 1, 6, 49, 22, 399779, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='windfarm',
            name='owner',
            field=models.ManyToManyField(blank=True, null=True, related_name='owners', to='player.Player'),
        ),
        migrations.AlterField(
            model_name='windfarm',
            name='service',
            field=models.ManyToManyField(blank=True, null=True, related_name='service_providers', to='player.Player'),
        ),
        migrations.AlterField(
            model_name='windfarm',
            name='tec_operator',
            field=models.ManyToManyField(blank=True, null=True, related_name='tec_operators', to='player.Player'),
        ),
    ]