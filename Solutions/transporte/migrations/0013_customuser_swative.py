# Generated by Django 4.0 on 2024-02-10 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transporte', '0012_ruta_swative'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='SwAtive',
            field=models.IntegerField(default=1),
        ),
    ]
