# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-07-20 12:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wind_farms', '0004_auto_20170720_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='windfarm',
            name='commisioning',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='windfarm',
            name='dismantling',
            field=models.DateField(blank=True, null=True),
        ),
    ]
