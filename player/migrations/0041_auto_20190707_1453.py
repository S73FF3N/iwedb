# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-07-07 14:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0040_player_head_organisation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='head_organisation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='headed_organisations', to='player.Player'),
        ),
    ]
