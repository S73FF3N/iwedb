# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-07-09 10:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turbine', '0019_servicelocation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicelocation',
            name='name',
            field=models.CharField(db_index=True, default='Osnabrück', max_length=100),
        ),
    ]
