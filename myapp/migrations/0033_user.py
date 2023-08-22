# Generated by Django 4.2.4 on 2023-08-14 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0032_remove_usuario_cargo_remove_usuario_curp_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id_user', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=25)),
                ('apellido', models.CharField(max_length=50)),
                ('telefono', models.CharField(max_length=15)),
                ('password', models.CharField(default='', max_length=20)),
            ],
        ),
    ]
