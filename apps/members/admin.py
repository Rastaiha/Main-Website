import imp
from django.contrib import admin
from .models import RastaMember,Term


@admin.register(RastaMember)
class MemberAdmin(admin.ModelAdmin):
    fields = ['name', 'education', 'role', 'photo_visible', 'photo_hidden','term']

@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    fields = ['name', 'start', 'end',]
