# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-08-24 11:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0014_auto_20170824_0851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wec_typ',
            name='nr_blades',
            field=models.IntegerField(blank=True, default=3, null=True, verbose_name='Amount of blades'),
        ),
        migrations.AlterField(
            model_name='wec_typ',
            name='product_web',
            field=models.URLField(blank=True, null=True, verbose_name='Product web page'),
        ),
    ]
