# Generated by Django 4.2.4 on 2023-10-13 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0041_venta_metodo_de_pago'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='codigo_barras',
            field=models.CharField(default='', max_length=20, unique=True),
        ),
    ]
