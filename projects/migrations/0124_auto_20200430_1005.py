# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2020-04-30 10:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0123_auto_20200430_0915'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expert_report',
            name='turbine',
        ),
        migrations.AddField(
            model_name='turbine_customerquestionnaire',
            name='expert_report',
            field=models.FileField(blank=True, help_text='Kindly upload the current expert inspection report of the WTG', upload_to='customer_questionnaire/expert_reports/', verbose_name='Expert Report'),
        ),
        migrations.DeleteModel(
            name='Expert_Report',
        ),
    ]
