from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit
from django import forms
from django.forms import TextInput

from mailing.models import Mailing, Mail


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
            Fieldset('Рассылка', 'first_dispatch', 'last_mailing', 'periodicity', 'number_clients', ),
            Submit('submit', 'Сохранить', css_class='button white'), )

    class Meta:
        model = Mailing
        fields = ('first_dispatch', 'last_mailing', 'periodicity', 'number_clients')
        widgets = {
            'first_dispatch': TextInput(attrs={'placeholder': 'Введите дату первой отправки'}),
            'last_mailing': TextInput(attrs={'placeholder': 'Введите дату последней отправки'}),
            'periodicity': TextInput(
                attrs={'placeholder': 'Введите периодичность 1(ежедневно), 2(еженедельно), 3(ежемесячно)'}),
            'number_clients': TextInput(
                attrs={'placeholder': 'Список клиентов в последствии можно дополнить'}),
        }

    def clean_name(self):
        cleaned_data = self.cleaned_data.get('periodicity')

        if cleaned_data == 1 or 2 or 3:
            return cleaned_data
        else:
            raise forms.ValidationError('Ошибка, не верные данные')


class MailForm(VisualFormMixin, forms.ModelForm):
    class Meta:
        model = Mail
        fields = ('subject_mail', 'text_mail')

# class ClientForm(forms.ModelForm):
#     class Meta:
#         model = Client
#         fields = ('contact_email', 'full_name', 'comment')
