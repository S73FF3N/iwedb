# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-05-16 04:47
from __future__ import unicode_literals

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0007_person'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='phone2',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True),
        ),
    ]