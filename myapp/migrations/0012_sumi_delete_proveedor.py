# Generated by Django 4.2.4 on 2023-08-04 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_remove_suministro_id_proveedor'),
    ]

    operations = [
        migrations.CreateModel(
            name='sumi',
            fields=[
                ('id_sumi', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=30)),
            ],
        ),
        migrations.DeleteModel(
            name='Proveedor',
        ),
    ]