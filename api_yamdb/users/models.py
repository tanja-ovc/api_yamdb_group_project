from django.db import models
from django.contrib.auth.models import (
    AbstractUser, UserManager
)


class MyUserManager(UserManager):
    def create_superuser(self, email, username, role, bio, password=None):
        user = self.create_user(
            email=email,
            username=username,
            is_staff=True,
            is_superuser=True,
            role='admin',
            bio=bio,
        )
        user.is_admin = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class MyUser(AbstractUser):
    email = models.EmailField(help_text='email address', blank=False, unique=True)
    bio = models.TextField(max_length=1000, blank=True)
    is_admin = models.BooleanField(default=False)
    confirmation_code = models.CharField(max_length=20, default=None, blank=True, null=True)

    ROLE_CHOICE = [
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Админ')
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICE, default='user')

    objects = MyUserManager()
