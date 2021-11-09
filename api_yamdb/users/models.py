from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractUser
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('У пользователя должен быть email')

        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.create_user(email=email, is_staff=True, is_superuser=True, **kwargs)
        user.is_admin = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class MyUser(AbstractUser):
    email = models.EmailField(
        verbose_name='email адрес',
        max_length=255,
        unique=True,
    )
    bio = models.TextField(max_length=1000, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    ROLE_CHOICE = [
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Админ')
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICE, default='user')

    objects = MyUserManager()
