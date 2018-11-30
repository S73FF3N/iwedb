# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-09-30 16:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0026_auto_20180912_1007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='adress',
            field=models.CharField(blank=True, default='', help_text='Enter the postal address', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='player',
            name='city',
            field=models.CharField(blank=True, default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='player',
            name='country',
            field=models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, to='wind_farms.Country'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='player',
            name='customer_code',
            field=models.CharField(blank=True, default='', help_text="Enter the customer code acc. to 'Projektübersicht'", max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='player',
            name='mail',
            field=models.EmailField(blank=True, default='', max_length=80),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='player',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, default='', help_text='Enter the phone number beginning with +', max_length=128),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='player',
            name='postal_code',
            field=models.CharField(blank=True, default='', max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='player',
            name='web',
            field=models.URLField(blank=True, default='', help_text='Enter a vaild web address incl. http://'),
            preserve_default=False,
        ),
    ]