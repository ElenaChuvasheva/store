# Generated by Django 4.2 on 2023-04-05 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_products_images'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(default=1, upload_to='products/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subcategory',
            name='image',
            field=models.ImageField(default=1, upload_to='products/'),
            preserve_default=False,
        ),
    ]
