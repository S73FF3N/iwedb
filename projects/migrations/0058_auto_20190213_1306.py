# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-02-13 13:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0057_auto_20190213_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offernumber',
            name='created',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
    ]
