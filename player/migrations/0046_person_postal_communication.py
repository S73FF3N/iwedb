# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2020-07-14 07:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0045_auto_20200714_0656'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='postal_communication',
            field=models.BooleanField(default=False, verbose_name='Postal communication preferred?'),
        ),
    ]
