from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView

from mailing.forms import MailingForm, ClientForm
from mailing.models import Mailing, Client


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:home')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Mailing, Client, form=ClientForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset_client'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset_client'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset_client = self.get_context_data()['formset_client']
        self.object = form.save()
        if formset_client.is_valid():
            formset_client.instance = self.object
            formset_client.save()

        return super().form_valid(form)



def home(request):
    return render(request, 'mailing/index.html')
