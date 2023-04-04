import uuid

from django.db import models


class Category(models.Model):
    name = models.CharField(unique=True, verbose_name='Название', max_length=256)
    slug = models.SlugField(unique=True, verbose_name='Адрес')

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

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    name = models.CharField(unique=True, verbose_name='Название', max_length=256)
    slug = models.SlugField(unique=True, verbose_name='Адрес')
    price = models.DecimalField(max_digits=6, decimal_places=2,
                                verbose_name='Цена')
    subcategory = models.ForeignKey(Subcategory, related_name='products',
                                    on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('subcategory',)

    def __str__(self):
        return self.name
