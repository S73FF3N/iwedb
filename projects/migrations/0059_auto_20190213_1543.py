# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-02-13 15:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0058_auto_20190213_1306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offernumber',
            name='amount',
            field=models.PositiveIntegerField(blank=True, help_text='Amount of turbines included in this project.', null=True),
        ),
        migrations.AlterField(
            model_name='offernumber',
            name='number',
            field=models.CharField(db_index=True, help_text='Offer Number generated automatically to ensure its uniqueness.', max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='offernumber',
            name='sales_manager',
            field=models.ForeignKey(blank=True, help_text='Who is the responsible Sales Manager?', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='offernumber',
            name='wind_farm',
            field=models.CharField(blank=True, help_text='Specify the wind farm which belongs to this offer number', max_length=50, null=True),
        ),
    ]