# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-03-07 09:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0037_auto_20190219_1044'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='player',
            options={'ordering': ('name',), 'permissions': (('comment_on_person', 'Can comment on persons'),)},
        ),
    ]
