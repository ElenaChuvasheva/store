# Generated by Django 4.2 on 2023-04-06 12:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_cart'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'verbose_name': 'Продукт в корзине', 'verbose_name_plural': 'Корзина'},
        ),
        migrations.AlterField(
            model_name='cart',
            name='amount',
            field=models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(limit_value=1, message='Количество не может быть меньше 1')], verbose_name='Количество'),
        ),
        migrations.AddConstraint(
            model_name='cart',
            constraint=models.UniqueConstraint(fields=('user', 'product'), name='unique_user_product'),
        ),
    ]
