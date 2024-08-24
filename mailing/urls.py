from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import MailingCreateView, confirm_mailing, MailingListView

app_name = MailingConfig.name

urlpatterns = [
    path('', MailingListView.as_view(), name='mailing_list'),
    path('add-mailing', MailingCreateView.as_view(), name='create_mailing'),
    path('confirm-create-mailing', confirm_mailing, name='confirm_create_mailing'),
]
