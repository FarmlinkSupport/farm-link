# Generated by Django 5.1 on 2024-09-15 20:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('company_name', models.CharField(max_length=50)),
                ('company_address', models.CharField(max_length=100)),
                ('company_zipcode', models.CharField(max_length=6)),
                ('gst_no', models.CharField(max_length=15)),
                ('is_verified', models.BooleanField(default=False)),
            ],
        ),
    ]
