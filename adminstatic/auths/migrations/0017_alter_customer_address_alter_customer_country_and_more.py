# Generated by Django 4.2.11 on 2024-05-12 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0016_customer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='country',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='state',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
