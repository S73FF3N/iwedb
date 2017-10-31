# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-07-28 19:50
from __future__ import unicode_literals

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0009_auto_20170726_1320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wec_typ',
            name='wind_class',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('Ia', 'IEC Ia'), ('Ib', 'IEC Ib'), ('IIa', 'IEC IIa'), ('IIb', 'IEC IIb'), ('IIIa', 'IEC IIIa'), ('IIIb', 'IEC IIIb'), ('S', 'IEC S'), ('IV', 'IEC IV')], default='Ia', max_length=10, null=True),
        ),
    ]