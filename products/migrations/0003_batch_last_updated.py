# Generated by Django 3.2.4 on 2021-06-23 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_batch_current_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='batch',
            name='last_updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
