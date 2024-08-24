from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from mailing.forms import MailingForm, MailForm
from mailing.models import Mailing, Mail


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:confirm_create_mailing')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        MailFormset = inlineformset_factory(Mailing, Mail, form=MailForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = MailFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = MailFormset(instance=self.object)

        return context_data

    def form_valid(self, form):
        formset_client = self.get_context_data()['formset']
        self.object = form.save()
        if formset_client.is_valid():
            formset_client.instance = self.object
            formset_client.save()

        return super().form_valid(form)


class MailingListView(ListView):
    model = Mailing


class MailingDetailView(DetailView):
    model = Mailing


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        MailFormset = inlineformset_factory(Mailing, Mail, form=MailForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = MailFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = MailFormset(instance=self.object)

        return context_data

    def form_valid(self, form):
        formset_client = self.get_context_data()['formset']
        self.object = form.save()
        if formset_client.is_valid():
            formset_client.instance = self.object
            formset_client.save()

        return super().form_valid(form)


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')


def confirm_mailing(request):
    return render(request, 'mailing/conf_create_mailing.html')
