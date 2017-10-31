# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-08-01 06:27
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0003_auto_20170801_0627'),
        ('wind_farms', '0015_auto_20170731_1312'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='windfarm',
            name='operator',
        ),
        migrations.AddField(
            model_name='windfarm',
            name='com_operator',
            field=models.ManyToManyField(related_name='com_operators', to='player.Player'),
        ),
        migrations.AddField(
            model_name='windfarm',
            name='service',
            field=models.ManyToManyField(related_name='service_providers', to='player.Player'),
        ),
        migrations.AddField(
            model_name='windfarm',
            name='tec_operator',
            field=models.ManyToManyField(related_name='tec_operators', to='player.Player'),
        ),
        migrations.AlterField(
            model_name='windfarm',
            name='commisioning',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 8, 1, 6, 27, 14, 504267, tzinfo=utc), null=True, verbose_name='Commisioning date'),
        ),
        migrations.RemoveField(
            model_name='windfarm',
            name='developer',
        ),
        migrations.AddField(
            model_name='windfarm',
            name='developer',
            field=models.ManyToManyField(related_name='developers', to='player.Player'),
        ),
        migrations.AlterField(
            model_name='windfarm',
            name='dismantling',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 8, 1, 6, 27, 14, 504312, tzinfo=utc), null=True),
        ),
        migrations.RemoveField(
            model_name='windfarm',
            name='owner',
        ),
        migrations.AddField(
            model_name='windfarm',
            name='owner',
            field=models.ManyToManyField(related_name='owners', to='player.Player'),
        ),
    ]