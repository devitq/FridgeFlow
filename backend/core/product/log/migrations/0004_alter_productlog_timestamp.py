# Generated by Django 5.1.4 on 2025-01-12 11:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_log', '0003_remove_productlog_product_productlog_product_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productlog',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
