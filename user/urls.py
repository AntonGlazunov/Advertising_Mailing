from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from user.apps import UserConfig
from user.views import RegisterView, ProfileView, email_confirmation_sent, UserConfirmEmailView, email_confirmed, \
    email_confirmation_failed, UserForgotPasswordView, UserPasswordResetConfirmView, password_confirmed, \
    password_confirmation_failed, UserLoginView, UserListView, UserUpdateView

app_name = UserConfig.name
#
urlpatterns = [
    path('', UserLoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('email-confirmation-sent/', email_confirmation_sent, name='email_confirmation_sent'),
    path('confirm-email/<uidb64>/<token>/', UserConfirmEmailView.as_view(), name='confirm_email'),
    path('email-confirmed/', email_confirmed, name='email_confirmed'),
    path('confirm-email-failed/', email_confirmation_failed, name='email_confirmation_failed'),
    path('password_reset/', UserForgotPasswordView.as_view(), name='password_reset'),
    path('set-new-password/<uidb64>/<token>/<pas>', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-confirmed/', password_confirmed, name='password_confirmed'),
    path('confirm-password-failed/', password_confirmation_failed, name='password_confirmation_failed'),
    path('user_list/', UserListView.as_view(), name='user_list'),
    path('user_update/<int:pk>', UserUpdateView.as_view(), name='user_update'),
]
