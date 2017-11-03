# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-11-02 10:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0018_auto_20171028_1159'),
        ('components', '0007_auto_20171028_1218'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gearbox',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200)),
                ('slug', models.SlugField(max_length=200)),
                ('manufacturer', models.CharField(max_length=200)),
                ('image', models.ImageField(blank=True, upload_to='components/%Y/%m/%d')),
                ('description', models.TextField(blank=True)),
                ('weight_t', models.IntegerField(blank=True, null=True, verbose_name='Weight [t]')),
                ('ratio', models.IntegerField(blank=True, null=True)),
                ('stages', models.IntegerField(blank=True, null=True)),
                ('available', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('compatible_to', models.ManyToManyField(to='polls.WEC_Typ')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.AlterField(
            model_name='component',
            name='generator_type',
            field=models.CharField(choices=[('Asynchronous', 'Asyncronous'), ('Double fed induction generator', 'Double fed induction generator'), ('Seperate-exited synchronous', 'Seperate-exited synchronous'), ('Self-exited synchronous', 'Self-exited synchronous')], default='Asynchronous', max_length=20),
        ),
        migrations.AlterField(
            model_name='component',
            name='tower_type',
            field=models.CharField(choices=[('Lattice', 'Lattice'), ('Concrete', 'Concrete'), ('Hybrid', 'Hybrid'), ('Wood', 'Wood')], default='Hybrid', max_length=20),
        ),
        migrations.AlterIndexTogether(
            name='gearbox',
            index_together=set([('id', 'slug')]),
        ),
    ]