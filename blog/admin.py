from django.contrib import admin

from blog.models import Blog


@admin.register(Blog)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'views_count')
