# Generated by Django 4.2.11 on 2024-04-24 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0006_remove_message_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]