# Generated by Django 4.2.4 on 2023-08-04 17:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_remove_venta_cliente_productoventa_precio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='suministro',
            name='id_proveedor',
        ),
    ]