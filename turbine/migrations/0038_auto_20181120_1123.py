# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-11-20 11:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('turbine', '0037_auto_20181019_1246'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contract',
            options={'ordering': ['start_date'], 'permissions': (('can_view_contract_pdf', 'Can view contract pdf.'),)},
        ),
    ]