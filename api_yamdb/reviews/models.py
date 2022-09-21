from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser


CHOICES = (
    ('user', 'аутентифицированный пользователь'),
    ('moderator', 'модератор'),
    ('admin', 'администратор'),
)


class CustomUser(AbstractUser):
    bio = models.TextField(blank=True)
    role = models.CharField(
        max_length=15,
        choices=CHOICES,
        default='user'
    )


User = get_user_model()


class Categories(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class Genres(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class Titles(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    description = models.CharField(max_length=200)
    genre = models.ForeignKey(
        Genres,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles'
    )
    category = models.ForeignKey(
        Categories,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles'
    )

    def __str__(self):
        return self.title


