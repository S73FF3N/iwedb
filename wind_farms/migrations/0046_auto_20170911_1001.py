# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-09-11 10:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wind_farms', '0045_auto_20170911_0826'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='WEC',
            new_name='Turbine',
        ),
    ]
