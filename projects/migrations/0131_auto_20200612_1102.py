# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2020-06-12 11:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0130_auto_20200612_1026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graduatedprice',
            name='end_year',
            field=models.PositiveIntegerField(help_text="State the graduated price's end year", null=True, verbose_name='End Year'),
        ),
        migrations.AlterField(
            model_name='graduatedprice',
            name='start_year',
            field=models.PositiveIntegerField(help_text="State the graduated price's start year", null=True, verbose_name='Start year'),
        ),
    ]
