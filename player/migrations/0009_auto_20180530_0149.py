# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-05-30 01:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0008_person_phone2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='name',
            field=models.CharField(db_index=True, max_length=70, verbose_name='Name'),
        ),
    ]
