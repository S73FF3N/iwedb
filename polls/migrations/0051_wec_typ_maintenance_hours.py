# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-11-19 09:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0050_wec_typ_serviced_by_dwt'),
    ]

    operations = [
        migrations.AddField(
            model_name='wec_typ',
            name='maintenance_hours',
            field=models.IntegerField(blank=True, help_text='How many maintenance hours have to be substracted from the availability guarantee?', null=True),
        ),
    ]
