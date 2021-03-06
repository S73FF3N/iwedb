# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-02-11 12:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turbine', '0054_auto_20190207_1428'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contract',
            name='condition_based_inspection',
        ),
        migrations.RemoveField(
            model_name='contract',
            name='service_lift_repairs',
        ),
        migrations.AddField(
            model_name='contract',
            name='cms',
            field=models.BooleanField(default=False, help_text='Is a permanent condition monitoring included?'),
        ),
        migrations.AddField(
            model_name='contract',
            name='overhaul_working_equipment',
            field=models.BooleanField(default=False, help_text='Is the general overhaul of working equipment (winch, on-board crane, etc.) included?'),
        ),
        migrations.AddField(
            model_name='contract',
            name='safety_exchange',
            field=models.BooleanField(default=False, help_text='Is the repair of safety equipment (PSE, fire extinguisher, etc.) included?'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='safety_repairs',
            field=models.BooleanField(default=False, help_text='Is the repair of safety equipment (PSE, fire extinguisher, etc.) included?'),
        ),
    ]
