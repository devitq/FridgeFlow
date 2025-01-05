# Generated by Django 5.1.4 on 2025-01-05 16:11

import django.core.validators
import uuid
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('category', models.CharField(max_length=200)),
                ('manufacturer', models.CharField(max_length=200)),
                ('quantity', models.DecimalField(decimal_places=4, max_digits=11, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1000000)])),
                ('unit', models.CharField(max_length=50)),
                ('nutritional_value', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0')), django.core.validators.MaxValueValidator(Decimal('1000000'))])),
                ('total_net_weight', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0')), django.core.validators.MaxValueValidator(Decimal('1000000'))])),
                ('total_gross_weight', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0')), django.core.validators.MaxValueValidator(Decimal('1000000'))])),
                ('manufacture_date', models.DateField()),
                ('expiration_date', models.DateField()),
                ('notes', models.TextField(blank=True, max_length=1000, null=True)),
                ('allergens', models.TextField(blank=True, max_length=1000, null=True)),
            ],
        ),
    ]
