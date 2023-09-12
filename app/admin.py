from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class ContactAdmin(UserAdmin):
    fields = ['username', 'password', 'phonenumber', 'gender', 'birthdate', 'is_admin', 'is_active', 'is_shop_owner',
              'is_staff']
    fieldsets = None
    add_fieldsets = (
        (
            None,
            {
                "fields": ("phonenumber", "password1", "password2"),
            },
        ),
    )
    list_filter = ("gender", "is_shop_owner",)
    filter_horizontal = []
    list_display = ('phonenumber', 'gender', 'birthdate')

# Register your models here.
