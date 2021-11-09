from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import MyUser


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('email', 'bio', 'role', 'first_name', 'last_name',)

        def clean_password2(self):
            password1 = self.cleaned_data.get('password1')
            password2 = self.cleaned_data.get('password2')
            if password1 != password2:
                raise ValidationError('Пароли не совпадают')
            return password2

        def save(self, commit=True):
            user = super.save(commit=False)
            user.set_password(self.cleaned_data['password1'])
            if commit:
                user.save()
            return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('email', 'bio', 'role', 'first_name', 'last_name', 'is_active', 'is_admin',)


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'bio', 'role', 'first_name', 'last_name', 'is_active', 'is_admin',)
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('bio', 'first_name', 'last_name',)}),
        ('Permissions', {'fields': ('is_admin', 'role',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'bio',
                'first_name',
                'last_name',
                'is_admin',
                'role',
            ),
        }),
    )
    search_fields = ('email', 'bio', 'first_name', 'last_name',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(MyUser, UserAdmin)
admin.site.unregister(Group)
