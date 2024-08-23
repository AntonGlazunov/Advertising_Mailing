from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    contact_email = models.EmailField(verbose_name='E-mail')
    full_name = models.CharField(max_length=50, verbose_name='Ф.И.О.')
    comment = models.TextField(verbose_name='Коментарий', **NULLABLE)

    def __str__(self):
        return f'{self.contact_email} {self.full_name}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Mailing(models.Model):
    first_dispatch = models.DateField(auto_now=False, verbose_name='Дата первой отправки', **NULLABLE)
    periodicity = models.IntegerField(verbose_name='Периодичность')
    status = models.CharField(max_length=15, verbose_name='Статус')
    client = models.ForeignKey('mailing.Client', verbose_name='Клиент', on_delete=models.CASCADE, **NULLABLE)
    mail = models.OneToOneField('mailing.Mail', verbose_name='Сообщение', on_delete=models.CASCADE, **NULLABLE)
    last_dispatch = models.ForeignKey('mailing.LastDispatch', verbose_name='Последняя рассылка',
                                      on_delete=models.CASCADE, **NULLABLE)

    def __str__(self):
        return f'{self.status} {self.periodicity} {self.first_dispatch}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class Mail(models.Model):
    subject_mail = models.CharField(max_length=100, verbose_name='Тема письма')
    text_mail = models.TextField(verbose_name='Текст письма')

    def __str__(self):
        return f'{self.subject_mail} {self.text_mail}'

    class Meta:
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'


class LastDispatch(models.Model):
    date_last_dispatch = models.DateField(auto_now=False, verbose_name='Дата последней попытки', **NULLABLE)
    status = models.BooleanField(default=True, verbose_name='Статус отправки')
    mail_server_response = models.TextField(verbose_name='Ответ почтнового сервера', **NULLABLE)

    def __str__(self):
        return f'{self.status}'

    class Meta:
        verbose_name = 'Последняя рассылка'
        verbose_name_plural = 'Последние рассылки'