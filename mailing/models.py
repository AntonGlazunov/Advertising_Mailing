from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    contact_email = models.EmailField(verbose_name='E-mail')
    full_name = models.CharField(max_length=50, verbose_name='Ф.И.О.')
    comment = models.TextField(verbose_name='Коментарий', **NULLABLE)
    mailing = models.ForeignKey('mailing.Mailing', verbose_name='Рассылка', on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'{self.contact_email} {self.full_name}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Mailing(models.Model):
    name_dispatch = models.CharField(max_length=100, verbose_name='Наименование рассылки', unique=True)
    date_start_mailing = models.DateField(auto_now=False, verbose_name='Дата отправки')
    last_mailing = models.DateField(auto_now=False, verbose_name='Дата последней отправки')
    periodicity = models.IntegerField(verbose_name='Периодичность')
    status = models.CharField(max_length=15, verbose_name='Статус', default='создана')
    is_active = models.BooleanField(default=True, verbose_name='Разрешение на запуск рассылки')
    user = models.ForeignKey('user.User', verbose_name='Владелец', on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'{self.status} {self.periodicity} {self.date_start_mailing}'

    class Meta:
        permissions = [
            (
                'set_mailing',
                'Отмена рассылки'
            )
        ]
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class Mail(models.Model):
    subject_mail = models.CharField(max_length=100, verbose_name='Тема письма')
    text_mail = models.TextField(verbose_name='Текст письма')
    mailing = models.OneToOneField('mailing.Mailing', verbose_name='Рассылка', on_delete=models.CASCADE,
                                   related_name='mail')

    def __str__(self):
        return f'{self.subject_mail} {self.text_mail} '

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'


class LastDispatch(models.Model):
    date_last_dispatch = models.DateField(auto_now=False, verbose_name='Дата последней отправки', **NULLABLE)
    status = models.BooleanField(default=False, verbose_name='Статус отправки')
    mail_server_response = models.TextField(verbose_name='Ответ почтнового сервера', **NULLABLE)
    mailing = models.OneToOneField('mailing.Mailing', verbose_name='Рассылка',
                                   on_delete=models.CASCADE, related_name='lastdispatch')

    def __str__(self):
        return f'{self.status}'

    class Meta:
        verbose_name = 'Последняя рассылка'
        verbose_name_plural = 'Последние рассылки'
