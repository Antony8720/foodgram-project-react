from django.db import models
from django.core.validators import MinValueValidator
from users.models import User


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200
    )
    maesurement_init = models.CharField(
        max_length=200
    )


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
        blank=True
    )
    color = models.CharField(
        max_length=7,
        null=True,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Уникальный слаг'
    )


class Recipe(models.Model):
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Список ингредиентов'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Список id тегов'
    )
    image = models.ImageField(
        verbose_name='Картинка, закодированная в Base64'
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=200
    )
    text = models.CharField(
        verbose_name='Описание',
        max_length=200
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления(в минутах)',
        validators=[MinValueValidator(1)]
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
        )


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE
    )
    amount = models.IntegerField(
        verbose_name='Количество в рецепте'
    )
