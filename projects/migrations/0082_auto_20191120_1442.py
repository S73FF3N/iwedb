# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-11-20 14:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0081_auto_20191120_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='kundendaten',
            field=models.FileField(blank=True, upload_to='kundendatenblatt/', verbose_name='Customer Information Sheet'),
        ),
        migrations.AlterField(
            model_name='project',
            name='parkinfo',
            field=models.FileField(blank=True, upload_to='parkinfoblatt/', verbose_name='Wind Farm Information Sheet'),
        ),
    ]
