# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-08-24 12:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0003_auto_20170801_0627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='name',
            field=models.CharField(db_index=True, max_length=50, verbose_name='Name'),
        ),
    ]
