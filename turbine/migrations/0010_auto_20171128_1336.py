# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-11-28 13:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turbine', '0009_auto_20171123_1220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turbine',
            name='osm_id',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]
