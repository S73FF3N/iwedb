# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-09-10 12:00
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0028_remove_project_last_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='sales_manager',
            field=models.ForeignKey(default=7, on_delete=django.db.models.deletion.CASCADE, related_name='sales_manager', to=settings.AUTH_USER_MODEL),
        ),
    ]
