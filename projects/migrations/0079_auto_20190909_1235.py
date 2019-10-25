# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-09-09 12:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0078_remove_reminder_recipient'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ('-updated',), 'permissions': (('can_comment_projects', 'Can write comments on Sales projects.'), ('can_create_project_overview', 'Can create an overview of sales projects'), ('can_create_custom_export', 'Can create a custom export of sales projects'), ('project_to_contract', 'Can create contracts from won projects'), ('initialization', 'Can create initailization sheet'), ('change_sales_manager', 'Can change Sales Manager'), ('open_sales_tools', 'Can open Sales Tools'))},
        ),
    ]
