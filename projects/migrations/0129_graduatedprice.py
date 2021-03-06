# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2020-06-05 11:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('projects', '0128_auto_20200522_0840'),
    ]

    operations = [
        migrations.CreateModel(
            name='GraduatedPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('yearly_price', models.PositiveIntegerField(help_text='State the yearly remuneration per WTG', verbose_name='Yearly Price')),
                ('start_year', models.DateField(help_text="State the graduated price's start year", verbose_name='Start year')),
                ('duration', models.PositiveIntegerField(help_text="State the graduated price's duration in years", verbose_name='Duration')),
                ('object_id', models.PositiveIntegerField(null=True)),
                ('content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
        ),
    ]
