# Generated by Django 5.0.6 on 2025-06-01 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fichas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fichaacogida',
            name='fecha_recepcion',
            field=models.DateField(blank=True, null=True),
        ),
    ]
