# Generated by Django 4.2.11 on 2024-05-24 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0019_alter_review_options_purchase_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='ref',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
