# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-08-08 13:52
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0003_auto_20170801_0627'),
        ('wind_farms', '0026_auto_20170807_1327'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contract',
            name='partner',
        ),
        migrations.AlterField(
            model_name='contract',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 8, 8, 13, 52, 24, 578828, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='contract',
            name='start_date',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 8, 8, 13, 52, 24, 578772, tzinfo=utc), null=True),
        ),
        migrations.RemoveField(
            model_name='windfarm',
            name='com_operator',
        ),
        migrations.AddField(
            model_name='windfarm',
            name='com_operator',
            field=models.ManyToManyField(related_name='com_operators', to='player.Player'),
        ),
        migrations.AlterField(
            model_name='windfarm',
            name='commisioning',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 8, 8, 13, 52, 24, 579728, tzinfo=utc), null=True, verbose_name='Commisioning date'),
        ),
        migrations.AlterField(
            model_name='windfarm',
            name='developer',
            field=models.ManyToManyField(related_name='developers', to='player.Player'),
        ),
        migrations.AlterField(
            model_name='windfarm',
            name='dismantling',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 8, 8, 13, 52, 24, 579758, tzinfo=utc), null=True),
        ),
        migrations.RemoveField(
            model_name='windfarm',
            name='service',
        ),
        migrations.AddField(
            model_name='windfarm',
            name='service',
            field=models.ManyToManyField(related_name='service_providers', to='player.Player'),
        ),
        migrations.RemoveField(
            model_name='windfarm',
            name='tec_operator',
        ),
        migrations.AddField(
            model_name='windfarm',
            name='tec_operator',
            field=models.ManyToManyField(related_name='tec_operators', to='player.Player'),
        ),
    ]