# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2020-01-21 07:56
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0087_customerquestionnaire'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerquestionnaire',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2020, 1, 21, 7, 56, 23, 348904, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
