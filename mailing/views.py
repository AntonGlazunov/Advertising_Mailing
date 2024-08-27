from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from mailing.forms import MailingForm, MailForm, ClientForm
from mailing.models import Mailing, Mail, Client


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:confirm_create_mailing')

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


class MailingListView(ListView):
    model = Mailing


class MailingDetailView(DetailView):
    model = Mailing

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        pk_mailing = self.object.pk
        mailing = Mailing.objects.get(pk=pk_mailing)
        if mailing.periodicity == 1:
            context_data['periodicity'] = 'Ежедневно'
        elif mailing.periodicity == 2:
            context_data['periodicity'] = 'Еженедельно'
        elif mailing.periodicity == 3:
            context_data['periodicity'] = 'Ежемесячно'

        context_data['subject_text'] = Mail.objects.get(pk=pk_mailing)
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


def confirm_mailing(request):
    return render(request, 'mailing/conf_create_mailing.html')
