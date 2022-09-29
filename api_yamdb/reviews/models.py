from datetime import datetime
from turtle import title
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser


CHOICES = (
    ('user', 'аутентифицированный пользователь'),
    ('moderator', 'модератор'),
    ('admin', 'администратор'),
)


class CustomUser(AbstractUser):
    password = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(
        blank=True,
        null=True,
        default=True)
    is_staff = models.BooleanField(
        blank=True,
        null=True,
        default=False
    )
    is_superuser = models.BooleanField(
        blank=True,
        null=True,
        default=False
    )
    date_joined = models.DateTimeField(
        default=datetime.now,
        blank=True,
        null=True
    )
    bio = models.TextField(blank=True)
    role = models.CharField(
        max_length=15,
        choices=CHOICES,
        default='user'
    )
    confirmation_code = models.CharField(
        max_length=555,
        blank=True,
        null=True
    )
    token = models.CharField(
        max_length=555,
        blank=True,
        null=True,
    )


User = get_user_model()


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
    description = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        through='GenreTitle',
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles'
    )
    # review = models.ForeignKey(
    #     Review,
    #     on_delete=models.SET_NULL,
    #     blank=True,
    #     null=True,
    #     related_name='reviews',
    #     verbose_name="Обзор",
    # )

    def __str__(self):
        return self.title


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    text = models.TextField(help_text="Текст обзора")
    score = models.IntegerField()
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        blank=True,
        null=True,
    )
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
