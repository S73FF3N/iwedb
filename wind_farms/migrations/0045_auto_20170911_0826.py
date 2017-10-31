# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-09-11 08:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0017_auto_20170828_0715'),
        ('player', '0004_auto_20170824_1227'),
        ('wind_farms', '0044_auto_20170828_0928'),
    ]

    operations = [
        migrations.CreateModel(
            name='WEC',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wec_nr', models.CharField(db_index=True, max_length=15)),
                ('slug', models.SlugField(max_length=200)),
                ('hub_height', models.IntegerField(blank=True, default=100, null=True)),
                ('commisioning', models.DateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Commisioning date')),
                ('dismantling', models.DateField(blank=True, default=django.utils.timezone.now, null=True)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('offshore', models.CharField(choices=[('yes', 'yes'), ('no', 'no')], default='no', max_length=50)),
                ('status', models.CharField(choices=[('in production', 'in production'), ('under construction', 'under construction'), ('planned', 'planned'), ('dismantled', 'dismantled')], default='in production', max_length=50)),
                ('repowered', models.BooleanField(default=False)),
                ('available', models.BooleanField(default=True)),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
                ('com_operator', models.ManyToManyField(blank=True, related_name='wec_com_operators', to='player.Player', verbose_name='Commercial operator')),
                ('developer', models.ManyToManyField(blank=True, related_name='wec_developers', to='player.Player')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='wec_owners', to='player.Player')),
                ('service', models.ManyToManyField(blank=True, related_name='wec_service_providers', to='player.Player')),
                ('tec_operator', models.ManyToManyField(blank=True, related_name='wec_tec_operators', to='player.Player', verbose_name='Technicial operator')),
                ('wec_manufacturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wec_manufacturers', to='polls.Manufacturer')),
                ('wec_typ', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.WEC_Typ', verbose_name='Model')),
                ('wind_farm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wind_farms', to='wind_farms.WindFarm')),
            ],
            options={
                'ordering': ('wec_nr',),
            },
        ),
        migrations.AlterIndexTogether(
            name='wec',
            index_together=set([('id', 'slug')]),
        ),
    ]