# Generated by Django 5.1 on 2024-09-07 11:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0003_contractdeployment'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContractDeliveryStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_file', models.FileField(blank=True, null=True, upload_to='invoices/')),
                ('buyer_status', models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed')], default='Pending', max_length=20)),
                ('payment_status', models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed')], default='Pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('contract', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='contract.contract')),
            ],
        ),
    ]
