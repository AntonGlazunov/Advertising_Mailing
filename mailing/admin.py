from django.contrib import admin

from mailing.models import Client, Mail, LastDispatch, Mailing


@admin.register(Client)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('contact_email', 'full_name',)


@admin.register(Mailing)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('date_start_mailing', 'last_mailing', 'periodicity', 'status')


@admin.register(Mail)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('subject_mail', 'text_mail', 'mailing')


@admin.register(LastDispatch)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('date_last_dispatch', 'status', 'mail_server_response')
