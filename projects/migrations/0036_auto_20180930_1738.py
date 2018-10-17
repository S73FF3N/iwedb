# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-09-30 17:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0035_auto_20180930_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='file',
            field=models.FileField(blank=True, default='', upload_to='project_files/%Y/%m/%d/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
    ]
