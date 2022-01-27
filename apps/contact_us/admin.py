from django.contrib import admin
from apps.contact_us.models import UserFeedback


@admin.register(UserFeedback)
class UserFeedbackAdmin(admin.ModelAdmin):
    fields = ['name', 'text', 'email', 'type']
