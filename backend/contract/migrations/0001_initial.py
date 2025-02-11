# Generated by Django 5.1 on 2024-09-15 20:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tender', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contractfileipfs', models.CharField(max_length=100, null=True)),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Completed', 'Completed'), ('Terminated', 'Terminated')], default='Active', max_length=15)),
                ('payment_status', models.CharField(choices=[('Pending', 'Pending'), ('Buyer Paid', 'Buyer Paid'), ('Completed', 'Completed'), ('Failed', 'Failed')], default='Pending', max_length=20)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('contract_value', models.DecimalField(decimal_places=2, max_digits=15)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contract_buyer', to=settings.AUTH_USER_MODEL)),
                ('farmer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contract_farmer', to=settings.AUTH_USER_MODEL)),
                ('tender', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='contract_tender', to='tender.tender')),
            ],
        ),
        migrations.CreateModel(
            name='ContractBlockchain',
            fields=[
                ('contract', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='contract.contract')),
                ('blockchainaddress', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ContractDeliveryStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_file', models.FileField(blank=True, null=True, upload_to='invoices/')),
                ('buyer_status', models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed')], default='Pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('contract', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='contract.contract')),
            ],
        ),
        migrations.CreateModel(
            name='ContractDeployment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('farmeragreed', models.BooleanField(default=False)),
                ('buyeragreed', models.BooleanField(default=False)),
                ('deploy_status', models.BooleanField(default=False)),
                ('contract', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='deploy_contract', to='contract.contract')),
            ],
        ),
    ]
