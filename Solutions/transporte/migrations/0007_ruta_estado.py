# Generated by Django 4.0 on 2024-02-07 22:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transporte', '0006_ruta_vehiculo'),
    ]

    operations = [
        migrations.AddField(
            model_name='ruta',
            name='estado',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(limit_value=1)]),
        ),
    ]
