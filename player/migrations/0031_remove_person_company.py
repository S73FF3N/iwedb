# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-11-29 12:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0030_auto_20181026_1412'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='company',
        ),
    ]
