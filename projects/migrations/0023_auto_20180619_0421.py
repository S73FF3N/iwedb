# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-06-19 04:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0022_comment_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='ebt',
            field=models.DecimalField(blank=True, decimal_places=2, default=15, max_digits=4, null=True, verbose_name='EBT [€]'),
        ),
    ]
