# Generated by Django 4.2.4 on 2023-08-12 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0030_alter_devolucion_razon'),
    ]

    operations = [
        migrations.AddField(
            model_name='devolucion',
            name='total',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
