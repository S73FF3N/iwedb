# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-05-15 07:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0006_auto_20171029_1403'),
        ('projects', '0003_remove_project_wind_farm'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='player.Player'),
        ),
    ]
