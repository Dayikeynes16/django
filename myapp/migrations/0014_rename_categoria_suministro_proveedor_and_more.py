# Generated by Django 4.2.4 on 2023-08-04 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0013_rename_nombre_suministro_nombre_producto'),
    ]

    operations = [
        migrations.RenameField(
            model_name='suministro',
            old_name='categoria',
            new_name='proveedor',
        ),
        migrations.AddField(
            model_name='suministro',
            name='total',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]