# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-09-10 13:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0029_project_sales_manager'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='sales_manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales_manager', to=settings.AUTH_USER_MODEL),
        ),
    ]
