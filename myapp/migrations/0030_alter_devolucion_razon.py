# Generated by Django 4.2.4 on 2023-08-12 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0029_remove_devolucion_cantidad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devolucion',
            name='razon',
            field=models.CharField(choices=[('Producto en mal estado', 'Producto en mal estado'), ('exceso de grasa', 'Exceso de grasa'), ('producto equivocado', 'Producto equivocado'), ('otro', 'Otro')], default='otro', max_length=35),
        ),
    ]