from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=254,
        unique=True
    )
    username = models.CharField(
        verbose_name='Уникальный юзернейм',
        max_length=150,
        unique=True
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=150
    )
    follower = models.ManyToManyField(
        'self',
        blank=True,
        related_name='following',
        verbose_name='подписчик',
        symmetrical=False
    )
    favorite = models.ManyToManyField(
        'recipes.recipe',
        blank=True,
        related_name='users_favorited',
        verbose_name='Находится ли в избранном'
    )
    cart = models.ManyToManyField(
        'recipes.recipe',
        blank=True,
        related_name='users_added_to_cart',
        verbose_name='находится ли в корзине'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'password']

    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'], name='unique_user')
        ]
