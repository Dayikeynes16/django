# Generated by Django 4.2.4 on 2023-11-01 20:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0042_producto_codigo_barras'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='codigo_barras',
        ),
    ]