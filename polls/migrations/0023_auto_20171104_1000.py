# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-11-04 10:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0022_auto_20171104_0954'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='name',
            field=models.CharField(db_index=True, default='wind turbine name', max_length=50),
        ),
        migrations.AlterField(
            model_name='image',
            name='file',
            field=models.ImageField(upload_to='wec_types/%Y/%m/%d'),
        ),
    ]