# Generated by Django 2.2.19 on 2022-10-24 11:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredient',
            old_name='maesurement_init',
            new_name='measurement_unit',
        ),
    ]
