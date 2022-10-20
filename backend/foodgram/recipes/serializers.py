import base64
from rest_framework import serializers
from django.core.files.base import ContentFile

from .models import Recipe, Ingredient, Tag, RecipeIngredient


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_init')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeIngredient
        fields = ('amount', 'id', 'name', 'maesurement_init',)


class RecipeIngredientWriteSerializer(RecipeIngredientSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        required=True,
    )

    class Meta:
        model = RecipeIngredient
        fields = ('amount', 'id',)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)


class RecipeWriteSerializer(serializers.ModelSerializer):
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

    def input_data(self, validated_data, instance=None):
        validated_data['author'] = self.context.get('request').user
        try:
            ingredients = validated_data.pop('ingredients')
        except KeyError:
            ingredients = []
        try:
            tags = validated_data.pop('tags')
        except KeyError:
            tags = []
        if instance is None:
            recipe = Recipe.objects.create(**validated_data)
        else:
            recipe = instance
            for attr, value in validated_data.items():
                setattr(recipe, attr, value)
        if ingredients:
            recipe.ingredients.clear()
            for ingredient_item in ingredients:
                recipe.ingredients.add(
                    ingredient_item['id'],
                    through_defaults={'amount': ingredient_item['amount']},
                )
        if tags:
            recipe.tags.clear()
            for tag in tags:
                recipe.tags.add(tag)
        recipe.save()
        return recipe

    def create(self, validated_data):
        return self.input_data(validated_data)

    def update(self, validated_data, instance):
        return self.input_data(validated_data, instance)        
