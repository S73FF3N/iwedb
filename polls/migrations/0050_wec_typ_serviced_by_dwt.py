# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-06-05 11:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0049_auto_20190304_1040'),
    ]

    operations = [
        migrations.AddField(
            model_name='wec_typ',
            name='serviced_by_dwt',
            field=models.CharField(choices=[('No', 'No'), ('Basic', 'Basic'), ('Full Service', 'Full Service')], default='No', max_length=20, verbose_name='Serviced by DWT'),
        ),
    ]
