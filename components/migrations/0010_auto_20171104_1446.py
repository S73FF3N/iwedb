# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-11-04 14:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0023_auto_20171104_1000'),
        ('components', '0009_auto_20171102_1331'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gearbox',
            name='image',
        ),
        migrations.AddField(
            model_name='gearbox',
            name='image',
            field=models.ManyToManyField(to='polls.Image'),
        ),
        migrations.RemoveField(
            model_name='generator',
            name='image',
        ),
        migrations.AddField(
            model_name='generator',
            name='image',
            field=models.ManyToManyField(to='polls.Image'),
        ),
        migrations.RemoveField(
            model_name='tower',
            name='image',
        ),
        migrations.AddField(
            model_name='tower',
            name='image',
            field=models.ManyToManyField(to='polls.Image'),
        ),
    ]
