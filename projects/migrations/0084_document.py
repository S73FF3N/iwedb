# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-11-21 13:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0083_auto_20191120_1448'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('file', models.FileField(upload_to='document/%Y/%m/%d/')),
                ('version', models.CharField(max_length=8)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]