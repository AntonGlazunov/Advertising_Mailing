from random import shuffle

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from blog.models import Blog
from mailing.forms import MailingForm, MailForm, ClientForm, MailingModerForm
from mailing.models import Mailing, Mail, Client
from mailing.services import planning_mailing, cash_articles, cash_mailing


class MailingCreateView(LoginRequiredMixin, CreateView):
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
        mailing = form.save(commit=False)
        mailing.user = self.request.user
        mailing.save()
        planning_mailing()
        if formset_mail.is_valid() and formset_client.is_valid():
            formset_mail.instance = self.object
            formset_mail.save()
            formset_client.instance = self.object
            formset_client.save()
        return super().form_valid(form)


class MailingListView(ListView):
    model = Mailing


class MailingDetailView(LoginRequiredMixin, DetailView):
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


class MailingUpdateView(LoginRequiredMixin, UpdateView):
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

    def get_form_class(self):
        user = self.request.user
        if user == self.object.user or user.is_superuser:
            return MailingForm
        elif user.has_perm('mailing.set_mailing'):
            return MailingModerForm
        else:
            raise PermissionDenied


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        user = self.request.user
        success_url = self.get_success_url()
        if self.object.user == user or user.is_superuser:
            return super().form_valid(form)
        else:
            return HttpResponseRedirect(success_url)


def home(request):
    mailing = cash_mailing()
    quantity_mailing_active = len(mailing.exclude(status='завершена').filter(is_active=True))
    unique_client = len(Client.objects.distinct('contact_email'))
    articles = cash_articles()
    shuffle(articles)
    context = {
        'mailing_all': len(mailing),
        'mailing_active': quantity_mailing_active,
        'unique_client': unique_client,
        'articles': articles[:3]
    }
    return render(request, 'mailing/home.html', context)
