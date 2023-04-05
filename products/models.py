from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


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
                                 on_delete=models.PROTECT)
    image = models.ImageField(upload_to='products/',)

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(unique=True, verbose_name='Название', max_length=256)
    slug = models.SlugField(unique=True, verbose_name='Адрес')
    price = models.DecimalField(max_digits=6, decimal_places=2,
                                verbose_name='Цена',
                                validators=(MinValueValidator(
                                    limit_value=Decimal('0.01'), message='Цена не может быть меньше 1 коп'),))
    subcategory = models.ForeignKey(Subcategory, related_name='products',
                                    on_delete=models.PROTECT)
    image = models.ImageField(upload_to='products/',)


    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('subcategory',)

    def __str__(self):
        return self.name
