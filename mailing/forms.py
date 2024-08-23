from django import forms
from django.forms import TextInput

from mailing.models import Mailing, Client


# class VisualFormMixin:
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.form_class = 'blueForms'
#         self.helper.form_method = 'post'
#         self.helper.form_action = 'submit_survey'
#         self.helper.form_tag = False

class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ('first_dispatch', 'last_mailing', 'periodicity')
        widgets = {
            'first_dispatch': TextInput(attrs={'placeholder': 'Введите дату первой отправки'}),
            'last_mailing': TextInput(attrs={'placeholder': 'Введите дату последней отправки'}),
            'periodicity': TextInput(
                attrs={'placeholder': 'Введите периодичность 1(ежедневно), 2(еженедельно), 3(ежемесячно)'}),
        }

    def clean_name(self):
        cleaned_data = self.cleaned_data.get('periodicity')

        if cleaned_data == 1 or 2 or 3:
            return cleaned_data
        else:
            raise forms.ValidationError('Ошибка, не верные данные')


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('contact_email', 'full_name', 'comment')
