# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-05-17 06:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0012_auto_20180516_0817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='request_date',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='start_operation',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]
