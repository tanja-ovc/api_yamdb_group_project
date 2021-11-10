from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import MyUser


class UserAdmin(BaseUserAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'bio',
        'role',
        'first_name',
        'last_name',
        'is_active',
        'is_admin',
        'is_superuser',
    )
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('bio', 'first_name', 'last_name',)}),
        ('Permissions', {'fields': ('is_admin', 'role',)}),
    )

    search_fields = ('username', 'email', 'bio', 'first_name', 'last_name',)
    ordering = ('email',)


admin.site.register(MyUser, UserAdmin)
admin.site.unregister(Group)
