# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-05-15 07:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wind_farms', '0054_auto_20180503_0132'),
    ]

    operations = [
        migrations.AddField(
            model_name='windfarm',
            name='postal_code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
