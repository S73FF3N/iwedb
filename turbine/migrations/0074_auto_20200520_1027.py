# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2020-05-20 10:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turbine', '0073_auto_20200422_1408'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turbine',
            name='asset_management',
            field=models.ManyToManyField(blank=True, help_text="Specify the company which manages the turbine's asset", related_name='wec_asset_management', to='player.Player'),
        ),
    ]