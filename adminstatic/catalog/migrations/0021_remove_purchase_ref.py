# Generated by Django 4.2.11 on 2024-05-24 20:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0020_purchase_ref'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='ref',
        ),
    ]
