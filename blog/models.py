from django.db import models

from mailing.models import NULLABLE


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    slug = models.CharField(max_length=150, verbose_name='slug', **NULLABLE)
    content = models.TextField(verbose_name='Контент')
    image = models.ImageField(upload_to='blog/', verbose_name='Изображение', **NULLABLE)
    create_at = models.DateField(auto_now_add=True, verbose_name='Дата публикации')
    is_published = models.BooleanField(default=True, verbose_name='Признак публикации')
    views_count = models.IntegerField(default=0, verbose_name='Счетчик просмотров')

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'
