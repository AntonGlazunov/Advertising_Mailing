from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import home, MailingCreateView

app_name = MailingConfig.name

urlpatterns = [
    path('', home, name='home'),
    path('add-mailing', MailingCreateView.as_view(), name='create_mailing'),
]
