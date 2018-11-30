# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-07-04 12:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turbine', '0015_auto_20180704_0621'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contract',
            old_name='available',
            new_name='active',
        ),
        migrations.RemoveField(
            model_name='contract',
            name='contract_type',
        ),
        migrations.RemoveField(
            model_name='contract',
            name='turbine',
        ),
        migrations.AddField(
            model_name='contract',
            name='average_remuneration',
            field=models.DecimalField(decimal_places=2, default=35000, max_digits=8),
        ),
        migrations.AddField(
            model_name='contract',
            name='external_damages',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contract',
            name='farm_availability',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True),
        ),
        migrations.AddField(
            model_name='contract',
            name='main_components',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contract',
            name='name',
            field=models.CharField(db_index=True, default='V-TB-22270-24-02-01_Vollwartungsvertrag_WP XY', max_length=100),
        ),
        migrations.AddField(
            model_name='contract',
            name='remote_control',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contract',
            name='scheduled_maintenance',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contract',
            name='turbines',
            field=models.ManyToManyField(db_index=True, related_name='contracted_turbines', to='turbine.Turbine', verbose_name='Turbines'),
        ),
        migrations.AddField(
            model_name='contract',
            name='unscheduled_maintenance_material',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contract',
            name='unscheduled_maintenance_personnel',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contract',
            name='wtg_availability',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True),
        ),
    ]