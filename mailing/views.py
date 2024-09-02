import datetime

from django.forms import inlineformset_factory
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from mailing import scheduler
from mailing.forms import MailingForm, MailForm, ClientForm
from mailing.models import Mailing, Mail, Client
from mailing.services import planning_mailing


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        MailFormset = inlineformset_factory(Mailing, Mail, form=MailForm, extra=1)
        ClientFormset = inlineformset_factory(Mailing, Client, form=ClientForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset_client'] = ClientFormset(self.request.POST, instance=self.object)
            context_data['formset_mail'] = MailFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset_client'] = ClientFormset(instance=self.object)
            context_data['formset_mail'] = MailFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset_client = self.get_context_data()['formset_client']
        formset_mail = self.get_context_data()['formset_mail']
        self.object = form.save()
        if formset_mail.is_valid() and formset_client.is_valid():
            formset_mail.instance = self.object
            formset_mail.save()
            formset_client.instance = self.object
            formset_client.save()
            planning_mailing(self.object)
        return super().form_valid(form)


class MailingListView(ListView):
    model = Mailing


class MailingDetailView(DetailView):
    model = Mailing

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        mailing = Mailing.objects.get(pk=self.object.pk)
        if mailing.periodicity == 1:
            context_data['periodicity'] = 'Ежедневно'
        elif mailing.periodicity == 2:
            context_data['periodicity'] = 'Еженедельно'
        elif mailing.periodicity == 3:
            context_data['periodicity'] = 'Ежемесячно'

        if Mail.objects.get(mailing=mailing) is not None:
            context_data['mail_all'] = Mail.objects.get(mailing=mailing)
        else:
            context_data['mail_all'] = None
        return context_data


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        MailFormset = inlineformset_factory(Mailing, Mail, form=MailForm, extra=1)
        ClientFormset = inlineformset_factory(Mailing, Client, form=ClientForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset_client'] = ClientFormset(self.request.POST, instance=self.object)
            context_data['formset_mail'] = MailFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset_client'] = ClientFormset(instance=self.object)
            context_data['formset_mail'] = MailFormset(instance=self.object)

        return context_data

    def form_valid(self, form):
        formset_client = self.get_context_data()['formset_client']
        formset_mail = self.get_context_data()['formset_mail']
        self.object = form.save()
        if formset_client.is_valid() and formset_mail.is_valid():
            formset_mail.instance = self.object
            formset_client.instance = self.object
            formset_client.save()
            formset_mail.save()

        return super().form_valid(form)


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')
