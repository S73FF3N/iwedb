# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-02-13 12:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0055_auto_20190213_1230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offernumber',
            name='wec_typ',
            field=models.ManyToManyField(blank=True, help_text='Enter the turbine type (e.g. V90) not the manufacturer (e.g. Vestas)!', to='polls.WEC_Typ', verbose_name='Model'),
        ),
    ]