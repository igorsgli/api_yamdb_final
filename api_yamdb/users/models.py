from django.contrib.auth.models import AbstractUser
from django.db import models

from api.utils import get_confirmation_code


class CustomUser(AbstractUser):

    USER: str = 'user'
    MODERATOR: str = 'moderator'
    ADMIN: str = 'admin'

    CHOICES = (
        (USER, 'аутентифицированный пользователь'),
        (MODERATOR, 'модератор'),
        (ADMIN, 'администратор'),
    )

    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, help_text='Заполните биографию')
    role = models.CharField(
        max_length=max([len(item[0]) for item in CHOICES]),
        choices=CHOICES,
        default='user',
        help_text='Выберите роль'
    )
    confirmation_code = models.CharField(max_length=len(str(get_confirmation_code())), blank=True)

    class Meta:
        verbose_name = 'Пользователь'

    @property
    def is_admin(self):
        return (
            self.role == CustomUser.ADMIN
            or self.is_staff 
            or self.is_superuser
        )

    @property
    def is_moderator(self):
        return self.role == CustomUser.MODERATOR
