# Generated by Django 5.1.4 on 2025-01-03 19:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_remove_product_size'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='order',
            name='product',
        ),
        migrations.DeleteModel(
            name='Customer',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
    ]
