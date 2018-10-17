# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-09-12 10:07
from __future__ import unicode_literals

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0025_auto_20180910_0647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='function',
            field=models.CharField(blank=True, help_text='Role of the employee within its company', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='name',
            field=models.CharField(db_index=True, help_text='Surname and last name of the employee', max_length=50, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='person',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='Enter the phone number beginning with +', max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='phone2',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='Enter the phone number beginning with +', max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='adress',
            field=models.CharField(blank=True, help_text='Enter the postal address', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='customer_code',
            field=models.CharField(blank=True, help_text="Enter the customer code acc. to 'Projektübersicht'", max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='name',
            field=models.CharField(db_index=True, help_text="Enter the company's name", max_length=75, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='player',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='Enter the phone number beginning with +', max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='sector',
            field=models.ManyToManyField(help_text='Choose at least one sector', to='player.Sector'),
        ),
        migrations.AlterField(
            model_name='player',
            name='web',
            field=models.URLField(blank=True, help_text='Enter a vaild web address incl. http://', null=True),
        ),
    ]
