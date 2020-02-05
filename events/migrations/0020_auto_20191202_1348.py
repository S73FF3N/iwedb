# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-12-02 13:48
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0019_auto_20191202_1316'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ('-updated',)},
        ),
        migrations.AddField(
            model_name='event',
            name='updated',
            field=models.DateTimeField(auto_now=True, db_index=True, default=datetime.datetime(2019, 12, 2, 13, 48, 26, 488594, tzinfo=utc)),
            preserve_default=False,
        ),
    ]