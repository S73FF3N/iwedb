# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-06-13 04:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0014_auto_20180613_0248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='company',
            field=models.ManyToManyField(to='player.Player'),
        ),
    ]