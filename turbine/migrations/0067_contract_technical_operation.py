# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-09-05 10:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turbine', '0066_auto_20190716_1150'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='technical_operation',
            field=models.BooleanField(default=False, help_text='Is techncial operation included?'),
        ),
    ]
