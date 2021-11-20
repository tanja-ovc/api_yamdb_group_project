from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    def create_superuser(
            self,
            email,
            username,
            role='user',
            bio=None,
            password=None
    ):
        user = self.create_user(
            email=email,
            username=username,
            is_staff=True,
            is_superuser=True,
        )
        user.is_admin = True
        user.role = 'admin'
        user.set_password(password)
        user.confirmation_code = make_password(
            '00000', salt=None, hasher='argon2'
        )
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    email = models.EmailField(
        help_text='email address',
        blank=False,
        unique=True
    )
    bio = models.TextField(max_length=1000, blank=True)
    is_admin = models.BooleanField(default=False)
    confirmation_code = models.CharField(
        max_length=20,
        default=None,
        blank=True,
        null=True
    )

    ROLE_CHOICE = [
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Админ')
    ]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICE,
        default='user'
    )

    objects = CustomUserManager()
