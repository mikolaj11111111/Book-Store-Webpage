# Generated by Django 5.1.4 on 2024-12-09 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_category_options_product_size_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='size',
            field=models.CharField(blank=True, default='', max_length=2, null=True),
        ),
    ]
