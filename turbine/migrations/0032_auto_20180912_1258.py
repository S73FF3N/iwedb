# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-09-12 12:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turbine', '0031_auto_20180912_1257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turbine',
            name='hub_height',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Hub height in meters', max_digits=5, null=True),
        ),
    ]