# Generated by Django 4.2.11 on 2024-05-06 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='brand',
            options={'ordering': ['-date_created', '-date_updated']},
        ),
        migrations.AlterModelOptions(
            name='subcat',
            options={'ordering': ['-date_created', '-date_updated']},
        ),
        migrations.AddField(
            model_name='brand',
            name='date_updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
