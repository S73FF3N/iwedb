# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-07-24 08:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wind_farms', '0007_auto_20170724_0705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='windfarm',
            name='created',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='windfarm',
            name='offshore',
            field=models.CharField(choices=[('yes', 'yes'), ('no', 'no')], default='NO', max_length=50),
        ),
        migrations.AlterField(
            model_name='windfarm',
            name='status',
            field=models.CharField(choices=[('in production', 'in production'), ('under construction', 'under construction'), ('planned', 'planned'), ('dismantled', 'dismantled')], default='in production', max_length=50),
        ),
        migrations.AlterField(
            model_name='windfarm',
            name='updated',
            field=models.DateField(auto_now=True),
        ),
    ]
