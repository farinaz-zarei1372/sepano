from django.contrib import admin
from .models import Products


@admin.register(Products)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'inventory', 'price')


# Register your models here.
