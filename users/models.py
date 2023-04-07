from django.contrib.auth.models import AbstractUser
from django.db import models

MAX_LENGTH = 150
MAX_LENGTH_EMAIL = 254


class CustomUser(AbstractUser):
    """Кастомная модель User."""
    username = models.CharField(
        max_length=MAX_LENGTH,
        unique=True,
        blank=False,
        verbose_name='Nickname пользователя',
    )
    email = models.EmailField(
        max_length=MAX_LENGTH_EMAIL,
        unique=True,
        verbose_name='Адрес электронной почты'
    )
    first_name = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name='Имя пользователя'
    )
    last_name = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name='Фамилия пользователя'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
