from datetime import date

from apscheduler.schedulers.background import BackgroundScheduler
from dateutil.relativedelta import relativedelta
from django.core.mail import send_mail
from django_apscheduler.jobstores import DjangoJobStore

from config import settings
from mailing.models import Client, Mailing, LastDispatch

scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
scheduler.add_jobstore(DjangoJobStore(), "default")


def send_mailing(mailings):
    for mailing in mailings:
        list_clients_mail = []
        clients = Client.objects.filter(mailing=mailing)
        last_dispatch = LastDispatch()
        mailing.status = 'запущена'
        for client in clients:
            list_clients_mail.append(client.contact_email)
        if send_mail(mailing.mail.subject_mail, mailing.mail.text_mail, settings.EMAIL_HOST_USER, list_clients_mail,
                     fail_silently=False, ):
            last_dispatch.mailing = mailing
            last_dispatch.status = True
            if mailing.periodicity == 1:
                update_time = date.today() + relativedelta(days=+1)
                mailing.date_start_mailing = update_time
                if mailing.date_start_mailing > mailing.last_mailing:
                    mailing.status = 'завершена'
                mailing.save()
            elif mailing.periodicity == 2:
                update_time = date.today() + relativedelta(months=+1)
                mailing.date_start_mailing = update_time
                if mailing.date_start_mailing > mailing.last_mailing:
                    mailing.status = 'завершена'
                mailing.save()
            else:
                update_time = date.today() + relativedelta(years=+1)
                mailing.date_start_mailing = update_time
                if mailing.date_start_mailing > mailing.last_mailing:
                    mailing.status = 'завершена'
                mailing.save()
        else:
            last_dispatch.status = False
            last_dispatch.mail_server_response = 'Ошибка отправки'
        last_dispatch.date_last_dispatch = date.today()
        last_dispatch.save()


def planning_mailing():
    if len(scheduler.get_jobs()) == 0:
        scheduler.add_job(start_mailing, 'interval', minutes=2)
        scheduler.start()


def start_mailing():
    mailings = Mailing.objects.exclude(status='завершена').filter(date_start_mailing=date.today())
    if len(mailings) > 0:
        send_mailing(mailings)
