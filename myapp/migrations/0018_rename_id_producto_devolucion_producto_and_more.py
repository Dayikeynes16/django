# Generated by Django 4.2.4 on 2023-08-06 04:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0017_venta_abierta'),
    ]

    operations = [
        migrations.RenameField(
            model_name='devolucion',
            old_name='id_producto',
            new_name='producto',
        ),
        migrations.RenameField(
            model_name='devolucion',
            old_name='id_venta',
            new_name='venta',
        ),
        migrations.RemoveField(
            model_name='devolucion',
            name='cantidad_devuelta',
        ),
        migrations.RemoveField(
            model_name='devolucion',
            name='fecha_devolucion',
        ),
        migrations.RemoveField(
            model_name='devolucion',
            name='motivo',
        ),
        migrations.AddField(
            model_name='devolucion',
            name='cantidad',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='devolucion',
            name='comentarios',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='devolucion',
            name='fecha',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='devolucion',
            name='razon',
            field=models.CharField(choices=[('defectuoso', 'Producto defectuoso'), ('incorrecto', 'Producto incorrecto'), ('otro', 'Otro')], default='otro', max_length=20),
        ),
    ]
