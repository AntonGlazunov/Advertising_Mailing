from django.core.mail import send_mail

from config import settings
from mailing.models import Mail, Client
from mailing.scheduler import scheduler


def send_mailing(*args):
    list_clients_mail = []
    mail_ = Mail.objects.filter(mailing=args[0]).values()
    clients = Client.objects.filter(mailing=args[0])
    for client in clients:
        list_clients_mail.append(client.contact_email)
    send_mail(mail_[0]['subject_mail'], mail_[0]['text_mail'], settings.EMAIL_HOST_USER, list_clients_mail,
              fail_silently=False, )


def planning_mailing(mailing):
    scheduler.add_job(start_mailing, args=[mailing], run_date=mailing.first_dispatch, id=f'start {mailing.pk}')
    scheduler.add_job(stop_mailing, args=[mailing], run_date=mailing.last_mailing, id=f'stop {mailing.pk}')


def start_mailing(mailing):
    if mailing.periodicity == 1:
        scheduler.add_job(send_mailing, 'interval', day=1, id=mailing.pk, args=[mailing])
    elif mailing.periodicity == 2:
        scheduler.add_job(send_mailing, 'interval', week=1, id=mailing.pk, args=[mailing])
    elif mailing.periodicity == 3:
        scheduler.add_job(send_mailing, 'interval', month=1, id=mailing.pk, args=[mailing])


def stop_mailing(mailing):
    scheduler.remove_job(mailing.pk)
