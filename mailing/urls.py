from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import MailingCreateView, MailingListView, MailingUpdateView, MailingDetailView, \
    MailingDeleteView, home

app_name = MailingConfig.name

urlpatterns = [
    path('', home, name='home'),
    path('mailing-list', MailingListView.as_view(), name='mailing_list'),
    path('add-mailing', MailingCreateView.as_view(), name='create_mailing'),
    path('update-mailing/<int:pk>', MailingUpdateView.as_view(), name='update_mailing'),
    path('detail-mailing/<int:pk>', MailingDetailView.as_view(), name='detail_mailing'),
    path('delete_mailing/<int:pk>', MailingDeleteView.as_view(), name='delete_mailing'),
]
