from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.hashers import make_password
from .models import Product


@admin.register(Product)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'inventory', 'price')

# Register your models here.
