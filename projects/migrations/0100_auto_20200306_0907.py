# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2020-03-06 09:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0099_auto_20200304_1240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerquestionnaire',
            name='amount_wec',
            field=models.IntegerField(blank=True, help_text='Please provide the number of concerned turbines', null=True),
        ),
        migrations.AlterField(
            model_name='customerquestionnaire',
            name='bank_institute',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='customerquestionnaire',
            name='bic',
            field=models.CharField(blank=True, max_length=11),
        ),
        migrations.AlterField(
            model_name='customerquestionnaire',
            name='city',
            field=models.CharField(blank=True, help_text='Please specify the city where the wind farm is located', max_length=80),
        ),
        migrations.AlterField(
            model_name='customerquestionnaire',
            name='contractual_partner',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='customerquestionnaire',
            name='cp_city',
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AlterField(
            model_name='customerquestionnaire',
            name='cp_contact_person',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='customerquestionnaire',
            name='cp_legal_form',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='customerquestionnaire',
            name='cp_mail',
            field=models.EmailField(blank=True, max_length=80),
        ),
        migrations.AlterField(
            model_name='customerquestionnaire',
            name='cp_phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text="Format: '+49 541 38 05 38 100'", max_length=128),
        ),
        migrations.AlterField(
            model_name='customerquestionnaire',
            name='cp_postal_code',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='customerquestionnaire',
            name='cp_street_nr',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='customerquestionnaire',
            name='iban',
            field=models.CharField(blank=True, max_length=34),
        ),
        migrations.AlterField(
            model_name='customerquestionnaire',
            name='invoice_recipient',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='customerquestionnaire',
            name='ir_city',
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AlterField(
            model_name='customerquestionnaire',
            name='ir_contact_person',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='customerquestionnaire',
            name='ir_invoice_mail',
            field=models.EmailField(blank=True, max_length=80),
        ),
        migrations.AlterField(
            model_name='customerquestionnaire',
            name='ir_mail',
            field=models.EmailField(blank=True, max_length=80),
        ),
        migrations.AlterField(
            model_name='customerquestionnaire',
            name='ir_phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text="Format: '+49 541 38 05 38 100'", max_length=128),
        ),
        migrations.AlterField(
            model_name='customerquestionnaire',
            name='ir_postal_code',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='customerquestionnaire',
            name='ir_street_nr',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='customerquestionnaire',
            name='ir_tax_id',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='customerquestionnaire',
            name='postal_code',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='customerquestionnaire',
            name='sa_city',
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AlterField(
            model_name='customerquestionnaire',
            name='sa_company',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='customerquestionnaire',
            name='sa_information',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='customerquestionnaire',
            name='sa_postal_code',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='customerquestionnaire',
            name='sa_street_nr',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='customerquestionnaire',
            name='scope',
            field=models.CharField(choices=[('Servicevertrag', 'Servicevertrag'), ('TBF-Vertrag', 'TBF-Vertrag'), ('Auftragsarbeiten', 'Auftragsarbeiten'), ('Materialanfrage', 'Materialanfrage'), ('Support-Vertrag', 'Support-Vertrag')], default='Servicevertrag', help_text='Please select one suitable option', max_length=20, verbose_name='Desired Scope'),
        ),
        migrations.AlterField(
            model_name='customerquestionnaire',
            name='street_nr',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='customerquestionnaire',
            name='vat_nr',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='customerquestionnaire',
            name='wind_farm_name',
            field=models.CharField(blank=True, help_text='If multiple names exists, please provide them all', max_length=50),
        ),
        migrations.AlterField(
            model_name='turbine_customerquestionnaire',
            name='comissioning',
            field=models.DateField(blank=True, help_text='Date of comissioning'),
        ),
        migrations.AlterField(
            model_name='turbine_customerquestionnaire',
            name='control_system',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='turbine_customerquestionnaire',
            name='hub_height',
            field=models.DecimalField(blank=True, decimal_places=1, help_text='Hub height in meters', max_digits=5),
        ),
        migrations.AlterField(
            model_name='turbine_customerquestionnaire',
            name='manufacturer',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='polls.Manufacturer'),
        ),
        migrations.AlterField(
            model_name='turbine_customerquestionnaire',
            name='turbine_id',
            field=models.CharField(blank=True, help_text='Please provide the Turbine ID. If unknown, use this scheme: WindfarmName01.', max_length=25),
        ),
        migrations.AlterField(
            model_name='turbine_customerquestionnaire',
            name='turbine_model',
            field=models.ForeignKey(blank=True, help_text='Enter the turbine type (e.g. V90) not the manufacturer (e.g. Vestas)!', on_delete=django.db.models.deletion.CASCADE, to='polls.WEC_Typ'),
        ),
    ]
