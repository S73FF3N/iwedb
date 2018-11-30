# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-09-03 09:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0023_person_function'),
        ('turbine', '0021_servicelocation_postal_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='turbine',
            name='asset_management',
            field=models.ManyToManyField(blank=True, related_name='wec_asset_management', to='player.Player', verbose_name='Asset Management'),
        ),
    ]