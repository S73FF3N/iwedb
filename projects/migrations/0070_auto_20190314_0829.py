# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-03-14 08:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0069_auto_20190312_1255'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reminder',
            options={'ordering': ('-created',), 'permissions': (('can_set_reminders', 'Can set reminders.'),)},
        ),
    ]
