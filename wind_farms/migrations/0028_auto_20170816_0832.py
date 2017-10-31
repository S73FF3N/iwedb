# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-08-16 08:32
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0003_auto_20170801_0627'),
        ('wind_farms', '0027_auto_20170808_1352'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='actor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='player.Player'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contract',
            name='available',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='contract',
            name='contract_type',
            field=models.CharField(choices=[('commercial management', 'commercial management'), ('technical operations', 'technical operations'), ('service', 'service')], default='service', max_length=50),
        ),
        migrations.AddField(
            model_name='contract',
            name='created',
            field=models.DateField(auto_now_add=True, default=datetime.datetime(2017, 8, 16, 8, 32, 10, 98787, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contract',
            name='updated',
            field=models.DateField(auto_now=True, default=datetime.datetime(2017, 8, 16, 8, 32, 19, 387161, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contract',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 8, 16, 8, 31, 52, 16488, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='contract',
            name='start_date',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 8, 16, 8, 31, 52, 16410, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='windfarm',
            name='com_operator',
            field=models.ManyToManyField(blank=True, null=True, related_name='com_operators', to='player.Player'),
        ),
        migrations.AlterField(
            model_name='windfarm',
            name='commisioning',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 8, 16, 8, 31, 52, 18346, tzinfo=utc), null=True, verbose_name='Commisioning date'),
        ),
        migrations.AlterField(
            model_name='windfarm',
            name='developer',
            field=models.ManyToManyField(blank=True, null=True, related_name='developers', to='player.Player'),
        ),
        migrations.AlterField(
            model_name='windfarm',
            name='dismantling',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 8, 16, 8, 31, 52, 18381, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='windfarm',
            name='offshore',
            field=models.CharField(choices=[('yes', 'yes'), ('no', 'no')], default='no', max_length=50),
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