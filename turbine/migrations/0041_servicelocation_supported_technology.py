# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-12-03 13:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0047_auto_20180930_1740'),
        ('turbine', '0040_auto_20181127_0723'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicelocation',
            name='supported_technology',
            field=models.ForeignKey(default=7, on_delete=django.db.models.deletion.CASCADE, to='polls.Manufacturer'),
            preserve_default=False,
        ),
    ]
