# Generated by Django 4.0 on 2024-02-10 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transporte', '0010_alter_ruta_valortotal'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehiculo',
            name='SwAtive',
            field=models.IntegerField(default=1),
        ),
    ]
