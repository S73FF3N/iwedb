# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-03-06 12:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('turbine', '0055_auto_20190211_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='average_remuneration',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Enter the average remuneration per year and WTG of this contract', max_digits=8, null=True),
        ),
    ]
