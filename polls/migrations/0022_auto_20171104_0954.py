# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-11-04 09:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0021_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wec_typ',
            name='image',
        ),
        migrations.AddField(
            model_name='wec_typ',
            name='image',
            field=models.ManyToManyField(to='polls.Image'),
        ),
    ]
