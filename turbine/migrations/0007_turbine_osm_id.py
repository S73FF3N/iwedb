# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-11-20 12:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turbine', '0006_auto_20171101_1449'),
    ]

    operations = [
        migrations.AddField(
            model_name='turbine',
            name='osm_id',
            field=models.CharField(default='', max_length=25),
            preserve_default=False,
        ),
    ]
