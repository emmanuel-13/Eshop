# Generated by Django 4.2.11 on 2024-05-13 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0013_alter_purchase_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('deliver', 'deliver')], default='pending', max_length=50),
        ),
    ]
