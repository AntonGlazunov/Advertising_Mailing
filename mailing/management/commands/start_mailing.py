import datetime

from django.core.mail import send_mail
from django.core.management import BaseCommand
from django.db.models import Q

from config import settings
from mailing.models import Mail, Client, Mailing


class Command(BaseCommand):

    @staticmethod
    def send_mailing(mailing):
        list_clients_mail = []
        mail_ = Mail.objects.filter(mailing=mailing).values()
        clients = Client.objects.filter(mailing=mailing)
        for client in clients:
            list_clients_mail.append(client.contact_email)
        send_mail(mail_[0]['subject_mail'], mail_[0]['text_mail'], settings.EMAIL_HOST_USER, list_clients_mail,
                  fail_silently=False, )

    def handle(self, *args, **options):
        mailings = Mailing.objects.all()
        for mailing in mailings:
            str_last_mailing = str(mailing.last_mailing)
            list_last_mailing = str_last_mailing.split('-')
            datetime_last_mailing = datetime.date(int(list_last_mailing[0]), int(list_last_mailing[1]),
                                                    int(list_last_mailing[2]))
            if datetime_last_mailing >= datetime.date.today():
                Command.send_mailing(mailing)
                print('рассылка выполнена')
