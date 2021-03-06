# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2020-03-08 12:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0104_auto_20200308_1201'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerquestionnaire',
            name='scope_de',
            field=models.CharField(choices=[('Service Contract', 'Service Contract'), ('Technical Operations Contract', 'Technical Operations Contract'), ('Commisioned Work', 'Commisioned Work'), ('Request for Material', 'Request for Material'), ('Support Contract', 'Support Contract')], default='Servicevertrag', help_text='Please select one suitable option', max_length=20, null=True, verbose_name='Desired Scope'),
        ),
        migrations.AddField(
            model_name='customerquestionnaire',
            name='scope_en',
            field=models.CharField(choices=[('Service Contract', 'Service Contract'), ('Technical Operations Contract', 'Technical Operations Contract'), ('Commisioned Work', 'Commisioned Work'), ('Request for Material', 'Request for Material'), ('Support Contract', 'Support Contract')], default='Servicevertrag', help_text='Please select one suitable option', max_length=20, null=True, verbose_name='Desired Scope'),
        ),
        migrations.AlterField(
            model_name='customerquestionnaire',
            name='scope',
            field=models.CharField(choices=[('Service Contract', 'Service Contract'), ('Technical Operations Contract', 'Technical Operations Contract'), ('Commisioned Work', 'Commisioned Work'), ('Request for Material', 'Request for Material'), ('Support Contract', 'Support Contract')], default='Servicevertrag', help_text='Please select one suitable option', max_length=20, verbose_name='Desired Scope'),
        ),
        migrations.AlterField(
            model_name='project',
            name='awarding_reason',
            field=models.CharField(blank=True, choices=[('Price', 'Price'), ('Contract Design', 'Contract Design'), ('Experience with DWT', 'Experience with DWT'), ('Readiness', 'Readiness'), ('Regional Structures', 'Regional Structures'), ('Political Decision', 'Political Decision'), ('Liability', 'Liability')], help_text='Which reason lead to the awarding of the contract?', max_length=30, null=True),
        ),
    ]
