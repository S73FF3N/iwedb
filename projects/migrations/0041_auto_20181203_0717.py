# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-12-03 07:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0040_auto_20181126_2117'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='department',
        ),
        migrations.AddField(
            model_name='project',
            name='contract',
            field=models.CharField(choices=[('New Contract', 'New Contract'), ('Extension', 'Extension'), ('Upgrade', 'Upgrade'), ('Downgrade', 'Downgrade')], default='New Contract', max_length=30),
        ),
        migrations.AlterField(
            model_name='project',
            name='contract_type',
            field=models.CharField(choices=[('Basic Maintenance', 'Basic Maintenance'), ('Full Maintenance without MC', 'Full Maintenance without MC'), ('Full Maintenance with MC', 'Full Maintenance with MC'), ('Spare Parts', 'Spare Parts'), ('Other', 'Other')], default='Contract Overview', max_length=30),
        ),
    ]
