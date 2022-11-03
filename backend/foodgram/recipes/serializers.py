import base64

from django.core.files.base import ContentFile
from rest_framework import serializers
from users.serializers import MyUserSerializer

from .models import Ingredient, Recipe, RecipeIngredient, Tag


class Base64ImageField(serializers.ImageField):
    """Задает кастомное поле для картинки"""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиента"""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор промежуточной модели рецепт-ингредиент"""

    id = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount',)

    def get_id(self, obj):
        return obj.ingredient_id

    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit

    def get_name(self, obj):
        return obj.ingredient.name

    def get_amount(self, obj):
        return obj.amount


class RecipeIngredientWriteSerializer(RecipeIngredientSerializer):
    """Сериализатор промежуточной модели рецепт-ингредиент на запись"""

    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        required=True,
    )
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ('amount', 'id',)

    def validate_amount(self, value):
        if value < 1:
            raise serializers.ValidationError(
                'Убедитесь, что количество ингредиентов больше 1'
            )
        return value


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тэга"""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецепта"""

    tags = TagSerializer(
        many=True,
        required=True
    )
    author = MyUserSerializer(
        required=True
    )
    ingredients = RecipeIngredientSerializer(
        many=True,
        required=True
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart', 'name',
                  'image', 'text', 'cooking_time',)

    def get_is_favorited(self, obj):
        """Вычисление поля находится ли в избранном"""

        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        return user.favorite.filter(id=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        """Вычисление поля находится ли в корзине"""

        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        return user.cart.filter(id=obj.id).exists()


class RecipeWriteSerializer(serializers.ModelSerializer):
    """Сериализатор рецепта на запись"""

    ingredients = RecipeIngredientWriteSerializer(
        many=True,
        required=True
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        required=True
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('ingredients', 'tags', 'image', 'name',
                  'text', 'cooking_time',)

    def create(self, validated_data):
        """Создание объектов модели с проверкой на повтор ингредиентов"""

        validated_data['author'] = self.context.get('request').user
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient_item in ingredients:
            ing = ingredient_item.get('id').pk
            amt = ingredient_item.get('amount')
            if RecipeIngredient.objects.filter(
                ingredient_id=ing,
                amount=amt
            ).exists():
                raise serializers.ValidationError(
                    'Убедитесь, что отсутствуют повторяющиеся ингредиенты'
                )
            new_ri, _ = RecipeIngredient.objects.get_or_create(
                ingredient_id=ing, amount=amt)
            recipe.ingredients.add(new_ri)
        for tag in tags:
            recipe.tags.add(tag)
        recipe.save()
        return recipe

    def update(self, recipe, validated_data):
        """Редактирование объектов модели с проверкой на повтор ингредиентов"""

        if 'ingredients' in validated_data:
            ingredients = validated_data.pop('ingredients')
            recipe.ingredients.clear()
            for ingredient_item in ingredients:
                ing = ingredient_item.get('id')
                amt = ingredient_item.get('amount')
                if RecipeIngredient.objects.filter(
                    ingredient_id=ing,
                    amount=amt
                ).exists():
                    raise serializers.ValidationError(
                        'Убедитесь, что отсутствуют повторяющиеся ингредиенты'
                    )
                new_ri, _ = RecipeIngredient.objects.get_or_create(
                    ingredient_id=ing, amount=amt)
                recipe.ingredients.add(new_ri)
        if 'tags' in validated_data:
            tags = validated_data.pop('tags')
            recipe.tags.set(tags)
        return super().update(recipe, validated_data)

    def to_representation(self, Recipe):
        """Вывод данных с другого сериализатора после записи"""

        serializer = RecipeSerializer(instance=Recipe, context=self.context)
        return serializer.data


class RecipeSmallSerializer(serializers.ModelSerializer):
    """Сериализатор рецепта с частичными данными"""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time',)
