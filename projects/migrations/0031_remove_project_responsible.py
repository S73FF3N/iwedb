# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-09-11 06:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0030_auto_20180910_1310'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='responsible',
        ),
    ]