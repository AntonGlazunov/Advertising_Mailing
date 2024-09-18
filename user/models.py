from django.contrib.auth.models import AbstractUser
from django.db import models

from mailing.models import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    country = models.CharField(max_length=100, verbose_name='страна', **NULLABLE)
    is_block = models.BooleanField(default=False, verbose_name='Заблокирован')
    manager = models.BooleanField(default=False, verbose_name='Mенеджер')
    is_content_manager = models.BooleanField(default=False, verbose_name='Контент-менеджер')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        permissions = [
            (
                'set_user',
                'Блокировка пользователей'
            )
        ]
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
