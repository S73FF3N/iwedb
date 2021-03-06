# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-09-24 12:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0042_auto_20190707_1518'),
        ('events', '0008_auto_20190923_0801'),
    ]

    operations = [
        migrations.AddField(
            model_name='date',
            name='comment',
            field=models.CharField(blank=True, max_length=200, verbose_name='Kommentar'),
        ),
        migrations.AddField(
            model_name='date',
            name='event',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='events.Event', verbose_name='Gutachten'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='date',
            name='execution_date',
            field=models.DateField(blank=True, default=django.utils.timezone.now, verbose_name='Datum (ist)'),
        ),
        migrations.AddField(
            model_name='date',
            name='part_of_contract',
            field=models.CharField(choices=[('Ja', 'Ja'), ('Nein', 'Nein'), ('zustandsorientiert', 'zustandsorientiert'), ('einmalig', 'einmalig')], default='Ja', max_length=20, verbose_name='Vertragsbestandteil'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='date',
            name='service_provider',
            field=models.ForeignKey(default=512, on_delete=django.db.models.deletion.CASCADE, to='player.Player', verbose_name='Dienstleister'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='date',
            name='date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Datum (soll)'),
        ),
        migrations.AlterField(
            model_name='event',
            name='done',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Erste Durchführung (Soll)'),
        ),
    ]
