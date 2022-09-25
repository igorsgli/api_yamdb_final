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


class Review(models.Model):
    text = models.TextField(help_text="Текст обзора")
    score = models.IntegerField()
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    pub_date = models.DateTimeField(
        'Дата публикации обзора',
        auto_now_add=True
    )


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='comments',
        help_text="Автор"
    )
    pub_date = models.DateField(
        'Дата публикации комментария', auto_now_add=True
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name='comments',
        help_text="Обзор",
    )


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.IntegerField()
    description = models.CharField(max_length=200)
    genre = models.ForeignKey(
        Genre,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles'
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.SET_NULL, 
        blank=True,
        null=True,
        related_name='reviews',
        verbose_name="Обзор",
    )

    def __str__(self):
        return self.title
