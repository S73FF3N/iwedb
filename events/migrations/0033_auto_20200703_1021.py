# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2020-07-03 10:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0032_auto_20200520_1027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='date',
            name='status',
            field=models.CharField(choices=[('remaining', 'remaining'), ('ordered', 'ordered'), ('confirmed', 'confirmed'), ('scheduled', 'scheduled'), ('executed', 'executed'), ('report received', 'report received'), ('invoice received', 'invoice received'), ('closed', 'closed')], max_length=25),
        ),
    ]
