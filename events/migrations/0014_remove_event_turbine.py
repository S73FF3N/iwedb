# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-10-14 08:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0013_date_turbine'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='turbine',
        ),
    ]
