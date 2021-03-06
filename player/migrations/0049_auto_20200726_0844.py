# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2020-07-26 08:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0048_person_mailing_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='gender',
            field=models.CharField(choices=[('male', 'male'), ('female', 'female'), ('divers', 'divers')], db_index=True, default='divers', help_text='Gender of the employee', max_length=15),
        ),
        migrations.AlterField(
            model_name='person',
            name='postal_communication',
            field=models.BooleanField(default=False, help_text='For marketing communication: Check if the contact preferes postal over digital communication.', verbose_name='Postal communication'),
        ),
    ]
