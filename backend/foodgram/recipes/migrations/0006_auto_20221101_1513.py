# Generated by Django 2.2.19 on 2022-11-01 15:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_auto_20221027_1010'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipetag',
            old_name='ingredient',
            new_name='tag',
        ),
    ]
