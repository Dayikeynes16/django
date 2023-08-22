# Generated by Django 4.2.4 on 2023-08-02 03:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_remove_producto_descripcion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venta',
            name='fecha',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='ventasproducto',
            name='cantidad',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='ventasproducto',
            name='precio_de_venta',
            field=models.DecimalField(decimal_places=2, max_digits=7),
        ),
    ]