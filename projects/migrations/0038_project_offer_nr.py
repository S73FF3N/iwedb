# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-11-26 14:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0037_auto_20181105_1515'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='offer_nr',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]
