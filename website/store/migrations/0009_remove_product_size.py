# Generated by Django 5.1.4 on 2025-01-03 14:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_rename_conutry_profile_country_profile_zipcode'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='size',
        ),
    ]
