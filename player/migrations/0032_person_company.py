# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-11-29 12:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0031_remove_person_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='company',
            field=models.ManyToManyField(to='player.Player'),
        ),
    ]
