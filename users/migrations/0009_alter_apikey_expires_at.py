# Generated by Django 5.1.3 on 2025-01-02 05:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_apikey_expires_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apikey',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2026, 1, 2, 5, 37, 12, 349047)),
        ),
    ]
