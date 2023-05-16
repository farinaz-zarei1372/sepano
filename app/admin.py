from django.contrib import admin

from .models import Usermodel


@admin.register(Usermodel)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('username', 'phonenumber', 'gender', 'birthdate')

# Register your models here.
