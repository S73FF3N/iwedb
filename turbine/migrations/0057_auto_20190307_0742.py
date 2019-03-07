# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-03-07 07:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('turbine', '0056_auto_20190306_1240'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contract',
            options={'ordering': ['start_date'], 'permissions': (('can_view_contract_pdf', 'Can view contract pdf.'), ('can_terminate_contract', 'Can terminate contract'), ('can_create_custom_export_of_contracts', 'Can create a custom export of contracts'))},
        ),
    ]
