# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-01-10 09:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wind_farms', '0062_auto_20190107_0933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='windfarm',
            name='city',
            field=models.CharField(blank=True, help_text='Please specify ONE city', max_length=80),
        ),
    ]