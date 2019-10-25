# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-09-23 08:01
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_auto_20190923_0752'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='responsible',
            field=models.ForeignKey(help_text='Who is responsible?', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
