# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-05-15 04:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20180515_0413'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='wind_farm',
        ),
    ]