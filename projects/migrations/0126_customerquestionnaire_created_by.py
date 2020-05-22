# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2020-05-12 05:58
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0125_auto_20200508_1257'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerquestionnaire',
            name='created_by',
            field=models.ForeignKey(default=7, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]