from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from mailing.forms import MailingForm
from mailing.models import Mailing


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:home')


def home(request):
    return render(request, 'mailing/index.html')
