from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models.user import CustomUser


class CustomUserAdmin(UserAdmin):
    """
    to  modify display of the user sheet in the django admin console
    """
    list_display = ('username', 'email', 'age')

admin.site.register(CustomUser, CustomUserAdmin)
