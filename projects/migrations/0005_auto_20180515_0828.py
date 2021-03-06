# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-05-15 08:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_project_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='contract_signature',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='contract_type',
            field=models.CharField(choices=[('Contract Overview', 'Contract Overview'), ('Basic', 'Basic'), ('VWoGK', 'VWoGK'), ('VWmGKoR', 'VWmGKoR'), ('VWmGK', 'VWmGK'), ('Tender', 'Tender'), ('Remote Control', 'Remote Control'), ('TO', 'TO'), ('Spare Parts', 'Spare Parts'), ('Main Components', 'Main Components'), ('Support', 'Support'), ('Site Optimization', 'Site Optimization')], default='Contract Overview', max_length=30),
        ),
        migrations.AddField(
            model_name='project',
            name='department',
            field=models.CharField(choices=[('Service', 'Service'), ('Technical Operations', 'Technical Operations'), ('Remote Control', 'Remote Control')], default='Service', max_length=20),
        ),
        migrations.AddField(
            model_name='project',
            name='ebt',
            field=models.IntegerField(blank=True, default=350000, null=True, verbose_name='EBT [€]'),
        ),
        migrations.AddField(
            model_name='project',
            name='last_contact',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='project',
            name='price',
            field=models.IntegerField(blank=True, default=35000, null=True, verbose_name='Price [€/WTG/year]'),
        ),
        migrations.AddField(
            model_name='project',
            name='request_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='project',
            name='responsible',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='run_time',
            field=models.IntegerField(blank=True, default=5, null=True, verbose_name='Runtime [years]'),
        ),
        migrations.AddField(
            model_name='project',
            name='start_operation',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
