# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2020-05-08 12:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0124_auto_20200430_1005'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customerquestionnaire',
            options={'permissions': (('non_customer_view', 'Can view all menues.'),)},
        ),
    ]
