# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2020-04-30 07:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0121_auto_20200430_0748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='turbine_customerquestionnaire',
            name='expert_report',
            field=models.ManyToManyField(blank=True, to='projects.Expert_Report'),
        ),
    ]
