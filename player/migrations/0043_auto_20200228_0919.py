# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2020-02-28 09:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0042_auto_20190707_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(upload_to='actor_files/%Y/%m/%d/', verbose_name='File'),
        ),
        migrations.AlterField(
            model_name='person',
            name='adress',
            field=models.CharField(blank=True, help_text='Enter the postal address', max_length=100, verbose_name='Address'),
        ),
        migrations.AlterField(
            model_name='person',
            name='city',
            field=models.CharField(blank=True, max_length=50, verbose_name='City'),
        ),
        migrations.AlterField(
            model_name='person',
            name='company',
            field=models.ManyToManyField(to='player.Player', verbose_name='Company'),
        ),
        migrations.AlterField(
            model_name='person',
            name='function',
            field=models.CharField(blank=True, help_text='Role of the employee within its company', max_length=50, verbose_name='Function'),
        ),
        migrations.AlterField(
            model_name='person',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='Enter the phone number beginning with +', max_length=128, verbose_name='Phone'),
        ),
        migrations.AlterField(
            model_name='person',
            name='phone2',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='Enter the phone number beginning with +', max_length=128, verbose_name='Phone'),
        ),
        migrations.AlterField(
            model_name='person',
            name='postal_code',
            field=models.CharField(blank=True, max_length=10, verbose_name='Postal Code'),
        ),
        migrations.AlterField(
            model_name='player',
            name='city',
            field=models.CharField(blank=True, max_length=50, verbose_name='City'),
        ),
        migrations.AlterField(
            model_name='player',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wind_farms.Country', verbose_name='Country'),
        ),
        migrations.AlterField(
            model_name='player',
            name='customer_code',
            field=models.CharField(blank=True, help_text="Enter the customer code acc. to 'Projektübersicht'", max_length=10, null=True, verbose_name='Customer Code'),
        ),
        migrations.AlterField(
            model_name='player',
            name='head_organisation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='player.Player', verbose_name='Head Organisation'),
        ),
        migrations.AlterField(
            model_name='player',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='Enter the phone number beginning with +', max_length=128, verbose_name='Phone'),
        ),
        migrations.AlterField(
            model_name='player',
            name='postal_code',
            field=models.CharField(blank=True, max_length=10, verbose_name='Postal Code'),
        ),
        migrations.AlterField(
            model_name='player',
            name='sector',
            field=models.ManyToManyField(help_text='Choose at least one sector', to='player.Sector', verbose_name='Sector'),
        ),
    ]
