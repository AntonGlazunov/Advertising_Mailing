import datetime

from django import forms
from django.forms import TextInput

from mailing.models import Mailing, Mail, Client


class StyleFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():

            if isinstance(field.widget, forms.widgets.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            elif isinstance(field.widget, forms.DateTimeInput):
                field.widget.attrs['class'] = 'form-control flatpickr-basic'
            elif isinstance(field.widget, forms.DateInput):
                field.widget.attrs['class'] = 'form-control datepicker'
            elif isinstance(field.widget, forms.TimeInput):
                field.widget.attrs['class'] = 'form-control flatpickr-time'
            elif isinstance(field.widget, forms.widgets.SelectMultiple):
                field.widget.attrs['class'] = 'form-control select2 select2-multiple'
            elif isinstance(field.widget, forms.widgets.Select):
                field.widget.attrs['class'] = 'form-control select2'
            else:
                field.widget.attrs['class'] = 'form-control'


class MailingForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ('name_dispatch', 'date_start_mailing', 'last_mailing', 'periodicity')
        widgets = {
            'date_start_mailing': TextInput(attrs={'placeholder': 'dd.mm.yyyy'}),
            'last_mailing': TextInput(attrs={'placeholder': 'dd.mm.yyyy'}),
            'periodicity': TextInput(
                attrs={'placeholder': '1(ежедневно), 2(еженедельно), 3(ежемесячно)'}),
        }

    def clean_first_dispatch(self):
        cleaned_data = self.cleaned_data.get('date_start_mailing')
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
        first_dispatch = self.cleaned_data.get('date_start_mailing')
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


class MailForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mail
        fields = ('subject_mail', 'text_mail')

    def clean_subject_mail(self):
        cleaned_data = self.cleaned_data.get('subject_mail')
        if cleaned_data is None:
            raise forms.ValidationError('Ошибка, поле не может быть пустым')
        return cleaned_data


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = ('contact_email', 'full_name', 'comment')
