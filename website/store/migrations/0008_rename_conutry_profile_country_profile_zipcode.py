# Generated by Django 5.1.4 on 2025-01-02 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_profile_old_cart'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='conutry',
            new_name='country',
        ),
        migrations.AddField(
            model_name='profile',
            name='zipcode',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
