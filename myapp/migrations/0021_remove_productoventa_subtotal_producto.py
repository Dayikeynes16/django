# Generated by Django 4.2.4 on 2023-08-06 06:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0020_remove_productoventa_precio_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productoventa',
            name='subtotal_producto',
        ),
    ]
