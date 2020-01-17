# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2020-01-17 14:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0022_auto_20200117_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='date',
            name='comment',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Comment'),
        ),
        migrations.AlterField(
            model_name='date',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Scheduled Date'),
        ),
        migrations.AlterField(
            model_name='date',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.Event', verbose_name='Expert Report'),
        ),
        migrations.AlterField(
            model_name='date',
            name='execution_date',
            field=models.DateField(blank=True, null=True, verbose_name='Execution Date'),
        ),
        migrations.AlterField(
            model_name='date',
            name='part_of_contract',
            field=models.CharField(blank=True, choices=[('yes', 'yes'), ('no', 'no'), ('condition based', 'condition based'), ('non-recurrent', 'non-recurrent')], max_length=20, null=True, verbose_name='Part of Contract'),
        ),
        migrations.AlterField(
            model_name='date',
            name='service_provider',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='player.Player', verbose_name='Service Provider'),
        ),
        migrations.AlterField(
            model_name='date',
            name='status',
            field=models.CharField(choices=[('remaining', 'remaining'), ('ordered', 'ordered'), ('enrolled', 'enrolled'), ('executed', 'executed'), ('report received', 'report received'), ('invoice received', 'invoice received'), ('closed', 'closed')], max_length=25),
        ),
        migrations.AlterField(
            model_name='date',
            name='turbine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='date_turbine', to='turbine.Turbine', verbose_name='Turbine'),
        ),
        migrations.AlterField(
            model_name='event',
            name='duration',
            field=models.CharField(choices=[('years', 'years'), ('month', 'month'), ('days', 'days')], max_length=10, verbose_name='Duration'),
        ),
        migrations.AlterField(
            model_name='event',
            name='responsible',
            field=models.ForeignKey(help_text='Who is responsible?', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Responsible'),
        ),
        migrations.AlterField(
            model_name='event',
            name='time_interval',
            field=models.CharField(choices=[('years', 'years'), ('month', 'month'), ('days', 'days')], max_length=10, verbose_name='Time interval'),
        ),
    ]
