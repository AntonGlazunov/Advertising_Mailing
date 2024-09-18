from django.contrib.auth import login
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView, LoginView
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import CreateView, UpdateView, ListView, DetailView

from user.forms import UserRegisterForm, UserProfileForm, UserForgotPasswordForm, UserAuthenticationForm, UserModerForm
from user.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'user/register.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        host = self.request.get_host()
        activation_url = f'http://{host}/user/confirm-email/{uid}/{token}'
        send_mail(
            'Подтверждение адреса электронной почты',
            f'Для подтверждения регистрации пройдите по ссылке {activation_url}',
            'skyproglazunov@yandex.ru',
            [user.email],  # Это поле "Кому" (можно указать список адресов)
            fail_silently=False,  # Сообщать об ошибках («молчать ли об ошибках?»)
        )
        return redirect('user:email_confirmation_sent')


def email_confirmation_sent(request):
    return render(request, 'user/email_confirmation_sent.html')


class UserConfirmEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('user:email_confirmed')
        else:
            return redirect('user:email_confirmation_failed')


def email_confirmed(request):
    return render(request, 'user/email_confirmed.html')


def email_confirmation_failed(request):
    return render(request, 'user/email_confirmation_failed.html')


class UserForgotPasswordView(PasswordResetView):
    """
    Представление по сбросу пароля по почте
    """
    form_class = UserForgotPasswordForm
    template_name = 'user/password_reset.html'
    success_url = reverse_lazy('mailing:mailing_list')
    success_message = 'Письмо с инструкцией по восстановлению пароля отправлена на ваш email'
    subject_template_name = 'user/email/new_password_subject_mail.txt'
    email_template_name = 'user/email/new_password_mail.html'


class UserPasswordResetConfirmView(View):
    def get(self, request, uidb64, token, pas):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.set_password(pas)
            user.save()
            return redirect('user:password_confirmed')
        else:
            return redirect('user:password_confirmation_failed')


def password_confirmed(request):
    return render(request, 'user/password_confirmed.html')


def password_confirmation_failed(request):
    return render(request, 'user/password_confirmation_failed.html')


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('mailing:mailing_list')

    def get_object(self, queryset=None):
        return self.request.user





class UserLoginView(LoginView):
    form_class = UserAuthenticationForm


class UserListView(ListView):
    model = User


class UserUpdateView(UpdateView):
    model = User
    form_class = UserModerForm
    template_name = 'user/user_form.html'
    success_url = reverse_lazy('mailing:mailing_list')


