# Generated by Django 4.2.11 on 2024-05-07 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_alter_subcat_options_remove_brand_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='icons',
        ),
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, default='../static/img/user.jpg', null=True, upload_to='icons'),
        ),
    ]
