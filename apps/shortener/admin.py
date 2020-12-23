from django.contrib import admin

from apps.shortener.models import Shortener


@admin.register(Shortener)
class ShortenerAdmin(admin.ModelAdmin):
    fields = ['main_url', 'shortened_url', 'clicks']
    readonly_fields = ['clicks']
    list_display = ['main_url', 'shortened_url', 'clicks']
