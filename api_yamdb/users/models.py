from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):

    USER: str = 'user'
    MODERATOR: str = 'moderator'
    ADMIN: str = 'admin'

    CHOICES = (
        (USER, 'аутентифицированный пользователь'),
        (MODERATOR, 'модератор'),
        (ADMIN, 'администратор'),
    )

    password = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(
        default=datetime.now(tz=timezone.utc), blank=True
    )
    bio = models.TextField(blank=True, help_text='Заполните биографию')
    role = models.CharField(
        max_length=15,
        choices=CHOICES,
        default='user',
        help_text='Выберите роль'
    )
    confirmation_code = models.CharField(max_length=555, blank=True)

    class Meta:
        verbose_name = 'Пользователь'

    @property
    def is_admin(self):
        return self.role == CustomUser.ADMIN

    @property
    def is_user(self):
        return self.role == CustomUser.USER

    @property
    def is_moderator(self):
        return self.role == CustomUser.MODERATOR
