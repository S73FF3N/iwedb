# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-10-06 09:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wind_farms', '0049_auto_20170919_0747'),
    ]

    operations = [
        migrations.AddField(
            model_name='windfarm',
            name='offshore',
            field=models.NullBooleanField(default=False),
        ),
    ]
