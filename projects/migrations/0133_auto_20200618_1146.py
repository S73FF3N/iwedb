# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2020-06-18 11:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0132_graduatedprice_id_in_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graduatedprice',
            name='id_in_project',
            field=models.IntegerField(default=-1, help_text='Graduated Price ID. Unique for each GP in a given Project', verbose_name='Graduated Price ID'),
        ),
    ]
