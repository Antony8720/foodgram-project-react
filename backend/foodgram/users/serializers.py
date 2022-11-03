import importlib

from django.db.models import Count
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from .models import User


class UserRegSerializer(UserCreateSerializer):
    """Сериализатор регистрации пользователя"""

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('email', 'id', 'password', 'username', 'first_name',
                  'last_name',)


class MyUserSerializer(UserSerializer):
    """Сериализатор пользователя"""

    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed')

    def get_is_subscribed(self, User):
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        return User.following.filter(id=user.id).exists()


class UserSubscribeSerializer(MyUserSerializer):
    """Сериализатор подписки на пользователя"""

    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count',)

    def get_recipes(self, User):
        recipes_limit = int(
            self.context.get('request').GET.get('recipes_limit', default=0)
        )
        if recipes_limit > 0:
            recipes = User.recipes.all()[:recipes_limit]
        else:
            recipes = User.recipes.all()
        serializer_class = getattr(
            importlib.import_module('recipes.serializers'),
            'RecipeSmallSerializer',
        )
        serializer = serializer_class(
            many=True,
            instance=recipes
        )
        return serializer.data

    @staticmethod
    def get_recipes_count(User):
        return User.recipes.aggregate(Count('id'))['id__count']
