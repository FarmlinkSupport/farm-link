# Generated by Django 5.1 on 2024-09-07 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contract', '0007_remove_contractdeliverystatus_payment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='payment_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Buyer Paid', 'Buyer Paid'), ('Completed', 'Completed'), ('Failed', 'Failed')], default='Pending', max_length=20),
        ),
    ]
