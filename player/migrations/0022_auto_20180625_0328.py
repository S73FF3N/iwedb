# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-06-25 03:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0021_auto_20180613_1021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='name',
            field=models.CharField(db_index=True, max_length=75, verbose_name='Name'),
        ),
    ]