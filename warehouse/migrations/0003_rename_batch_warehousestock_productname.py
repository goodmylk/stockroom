# Generated by Django 3.2.4 on 2021-06-25 14:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0002_warehousestock'),
    ]

    operations = [
        migrations.RenameField(
            model_name='warehousestock',
            old_name='batch',
            new_name='productname',
        ),
    ]
