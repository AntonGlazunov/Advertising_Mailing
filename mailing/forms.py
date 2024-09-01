import datetime

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from django import forms
from django.forms import TextInput

from mailing.models import Mailing, Mail, Client


class VisualFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'submit_survey'
        self.helper.form_tag = False


class MailingForm(VisualFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Fieldset('Рассылка', 'name_dispatch', 'first_dispatch', 'last_mailing', 'periodicity', ),
            Submit('submit', 'Сохранить', css_class='button white'), )

    class Meta:
        model = Mailing
        fields = ('name_dispatch', 'first_dispatch', 'last_mailing', 'periodicity')
        widgets = {
            'first_dispatch': TextInput(attrs={'placeholder': 'dd.mm.yyyy'}),
            'last_mailing': TextInput(attrs={'placeholder': 'dd.mm.yyyy'}),
            'periodicity': TextInput(
                attrs={'placeholder': '1(ежедневно), 2(еженедельно), 3(ежемесячно)'}),
        }

    def clean_first_dispatch(self):
        cleaned_data = self.cleaned_data.get('first_dispatch')
        str_first_dispatch = str(cleaned_data)
        list_first_dispatch = str_first_dispatch.split('-')
        datetime_first_dispatch = datetime.date(int(list_first_dispatch[0]), int(list_first_dispatch[1]),
                                                int(list_first_dispatch[2]))
        if datetime_first_dispatch < datetime.date.today():
            raise forms.ValidationError('Введите дату позже сегодняшней')
        return cleaned_data

    def clean_last_mailing(self):
        cleaned_data = self.cleaned_data.get('last_mailing')
        str_last_mailing = str(cleaned_data)
        list_last_mailing = str_last_mailing.split('-')
        datetime_last_mailing = datetime.date(int(list_last_mailing[0]), int(list_last_mailing[1]),
                                              int(list_last_mailing[2]))
        first_dispatch = self.cleaned_data.get('first_dispatch')
        str_first_dispatch = str(first_dispatch)
        list_first_dispatch = str_first_dispatch.split('-')
        datetime_first_dispatch = datetime.date(int(list_first_dispatch[0]), int(list_first_dispatch[1]),
                                                int(list_first_dispatch[2]))
        if datetime_last_mailing < datetime.date.today() or datetime_last_mailing < datetime_first_dispatch:
            raise forms.ValidationError('Не верная дата.')
        return cleaned_data

    def clean_periodicity(self):
        cleaned_data = self.cleaned_data.get('periodicity')
        if cleaned_data > 3:
            raise forms.ValidationError('Ошибка, введите число от 1 до 3')
        return cleaned_data


class MailForm(VisualFormMixin, forms.ModelForm):
    class Meta:
        model = Mail
        fields = ('subject_mail', 'text_mail')

    def clean_subject_mail(self):
        cleaned_data = self.cleaned_data.get('subject_mail')
        if cleaned_data is None:
            raise forms.ValidationError('Ошибка, поле не может быть пустым')
        return cleaned_data


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('contact_email', 'full_name', 'comment')
