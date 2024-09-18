from datetime import date

from apscheduler.schedulers.background import BackgroundScheduler
from dateutil.relativedelta import relativedelta
from django.core.cache import cache
from django.core.mail import send_mail
from django_apscheduler.jobstores import DjangoJobStore

from blog.models import Blog
from config import settings
from mailing.models import Client, Mailing, LastDispatch, Mail

scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)
scheduler.add_jobstore(DjangoJobStore(), "default")


def send_mailing(mailings):
    for mailing in mailings:
        list_clients_mail = []
        clients = Client.objects.filter(mailing=mailing)
        mail = Mail.objects.filter(mailing=mailing)
        last_dispatch = LastDispatch()
        if len(clients) > 0 and len(mail) > 0:
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
        else:
            mailing.status = 'запущена'
            last_dispatch.mailing = mailing
            last_dispatch.status = False
            last_dispatch.date_last_dispatch = date.today()
            last_dispatch.mail_server_response = 'Отсутвует письмо или клиенты'
            last_dispatch.save()
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


def planning_mailing():
    if len(scheduler.get_jobs()) == 0:
        scheduler.add_job(start_mailing, 'interval', minutes=2)
        scheduler.start()


def start_mailing():
    mailings = Mailing.objects.exclude(status='завершена').filter(date_start_mailing=date.today(), is_active=True)
    if len(mailings) > 0:
        send_mailing(mailings)


def cash_articles():
    if settings.CACHE_ENABLE:
        key = f'blog_list'
        article_list = cache.get(key)
        if article_list is None:
            articles = Blog.objects.all()
            article_list = []
            for article in articles:
                article_list.append(article)
            cache.set(key, article_list)
    else:
        articles = Blog.objects.all()
        article_list = []
        for article in articles:
            article_list.append(article)

    cash_blog = article_list
    return cash_blog


def cash_mailing():
    if settings.CACHE_ENABLE:
        key = f'mailing_list'
        mailing_list = cache.get(key)
        if mailing_list is None:
            mailing_list = Mailing.objects.all()
            cache.set(key, mailing_list)
    else:
        mailing_list = Mailing.objects.all()

    cash_mailings = mailing_list
    return cash_mailings


def cash_client():
    if settings.CACHE_ENABLE:
        key = f'client_list'
        client_list = cache.get(key)
        if client_list is None:
            client_list = len(Client.objects.distinct('contact_email'))
            cache.set(key, client_list)
    else:
        client_list = len(Client.objects.distinct('contact_email'))

    cash_clients = client_list
    return cash_clients
