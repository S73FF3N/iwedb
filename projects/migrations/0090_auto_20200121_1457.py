# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2020-01-21 14:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0089_auto_20200121_1442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerquestionnaire',
            name='amount_wec',
            field=models.IntegerField(help_text='Please provide the number of concerned turbines'),
        ),
        migrations.AlterField(
            model_name='customerquestionnaire',
            name='city',
            field=models.CharField(blank=True, help_text='Please specify the city where the wind farm is located', max_length=80),
        ),
        migrations.AlterField(
            model_name='customerquestionnaire',
            name='location_details',
            field=models.CharField(help_text='You can provide additional information', max_length=200),
        ),
        migrations.AlterField(
            model_name='customerquestionnaire',
            name='scope',
            field=models.CharField(choices=[('Servicevertrag', 'Servicevertrag'), ('TBF-Vertrag', 'TBF-Vertrag'), ('Auftragsarbeiten', 'Auftragsarbeiten'), ('Materialanfrage', 'Materialanfrage'), ('Support-Vertrag', 'Support-Vertrag')], default='Servicevertrag', help_text='Please select one suitable option', max_length=20),
        ),
    ]
