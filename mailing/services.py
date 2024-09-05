import datetime
import smtplib

from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import send_mail
from django_apscheduler.jobstores import DjangoJobStore

from config import settings
from mailing.models import Mail, Client, LastDispatch

scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
scheduler.add_jobstore(DjangoJobStore(), "default")


def print_hi(text):
    print(text)


def send_mailing(mailing):
    list_clients_mail = []
    mail_ = Mail.objects.filter(mailing=mailing).values()
    clients = Client.objects.filter(mailing=mailing)
    last_dispatch = LastDispatch.objects.get(mailing=mailing)
    for client in clients:
        list_clients_mail.append(client.contact_email)
    try:
        send_mail(mail_[0]['subject_mail'], mail_[0]['text_mail'], settings.EMAIL_HOST_USER, list_clients_mail,
                  fail_silently=False, )
        last_dispatch.date_last_dispatch = datetime.date.today()
    except smtplib.SMTPException:
        last_dispatch.mail_server_response = 'Ответ от почтового сервера'


def planning_mailing(mailing):
    list_first_dispatch = str(mailing.first_dispatch).split('-')
    datetime_first_dispatch = datetime.date(int(list_first_dispatch[0]), int(list_first_dispatch[1]),
                                            int(list_first_dispatch[2]))
    list_last_mailing = str(mailing.last_mailing).split('-')
    datetime_last_mailing = datetime.date(int(list_last_mailing[0]), int(list_last_mailing[1]),
                                          int(list_last_mailing[2]))
    scheduler.add_job(start_mailing, 'date', args=[mailing], run_date=datetime_first_dispatch, id=f'start {mailing.pk}')
    scheduler.add_job(stop_mailing, 'date', args=[mailing], run_date=datetime_last_mailing, id=f'stop {mailing.pk}')
    scheduler.start()


# def update_planning_mailing(mailing):
#     list_first_dispatch = str(mailing.first_dispatch).split('-')
#     datetime_first_dispatch = datetime.date(int(list_first_dispatch[0]), int(list_first_dispatch[1]),
#                                             int(list_first_dispatch[2]))
#     list_last_mailing = str(mailing.last_mailing).split('-')
#     datetime_last_mailing = datetime.date(int(list_last_mailing[0]), int(list_last_mailing[1]),
#                                           int(list_last_mailing[2]))
#     scheduler.add_job(start_mailing, args=[mailing], run_date=datetime_first_dispatch, id=f'start {mailing.pk}')
#     scheduler.add_job(print_hi(), run_date=datetime_first_dispatch, id=f'one_mail {mailing.pk}')
#     scheduler.add_job(stop_mailing, args=[mailing], run_date=datetime_last_mailing, id=f'stop {mailing.pk}')
#     scheduler.start()

def start_mailing(mailing):
    if mailing.periodicity == 1:
        print_hi(mailing.name_dispatch)
        mailing.status = 'запущена'
        scheduler.add_job(print_hi, 'interval', seconds=10, id=str(mailing.pk), args=[mailing.name_dispatch])
        scheduler.start()
    elif mailing.periodicity == 2:
        scheduler.add_job(send_mailing, 'interval', week=1, id=str(mailing.pk), args=[mailing])
        scheduler.start()
        mailing.status = 'запущена'
    elif mailing.periodicity == 3:
        scheduler.add_job(send_mailing, 'interval', month=1, id=str(mailing.pk), args=[mailing])
        scheduler.start()
        mailing.status = 'запущена'


def stop_mailing(mailing):
    scheduler.remove_job(str(mailing.pk))
    mailing.status = 'завершена'
