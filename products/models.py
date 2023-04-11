from datetime import datetime
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(unique=True, verbose_name='Название', max_length=256)
    slug = models.SlugField(unique=True, verbose_name='Адрес')
    image = models.ImageField(upload_to='products/',)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(unique=True, verbose_name='Название', max_length=256)
    slug = models.SlugField(unique=True, verbose_name='Адрес')
    category = models.ForeignKey(Category,
                                 related_name='subcategories',
                                 on_delete=models.PROTECT,
                                 verbose_name='Категория')
    image = models.ImageField(upload_to='products/',)

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
        ordering = ('category',)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(unique=True, verbose_name='Название', max_length=256)
    slug = models.SlugField(unique=True, verbose_name='Адрес')
    price = models.DecimalField(max_digits=6, decimal_places=2,
                                verbose_name='Цена',
                                validators=(MinValueValidator(
                                    limit_value=Decimal('0.01'),
                                    message='Цена не может быть меньше 1 коп'),
                                    ))
    subcategory = models.ForeignKey(Subcategory, related_name='products',
                                    on_delete=models.PROTECT,
                                    verbose_name='Подкатегория')
    image = models.ImageField(upload_to='products/',)


    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('subcategory__category', 'subcategory')

    def __str__(self):
        return self.name


class CartObject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='cart_of',
                             verbose_name='Пользователь')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='cart',
                                verbose_name='Продукт')
    amount = models.PositiveSmallIntegerField(verbose_name='Количество',
        validators=[
            MinValueValidator(limit_value=1,
                              message='Количество не может быть меньше 1')],
        default=1)
    
    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'product'), name='unique_user_product'),)
        ordering = ('-pk',)
