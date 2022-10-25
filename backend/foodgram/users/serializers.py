from django.db.models import Count
from rest_framework import serializers
from .models import User
from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.serializers import RecipeSmallSerializer


class UserRegSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('email', 'id', 'password', 'username', 'first_name',
                  'last_name',)


class MyUserSerializer(UserSerializer):
    is_subscried = serializers.BooleanField(default=False)

    class Meta(UserSerializer.Meta):
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscried')


class UserSubscribeSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count',)

    def get_recipes(self, User):
        recipes_limit = int(
            self.context.get('request').GET.get('recipes_limit',default=0)
        )
        if recipes_limit > 0:
            recipes = User.recipes.all()[:recipes_limit]
        else:
            recipes = User.objects.all()
        serializer_class = RecipeSmallSerializer
        serializer = serializer_class(
            many=True,
            instance=recipes
        )
        return serializer.data

    @staticmethod
    def get_recipes_count(User):
        return User.recipes.aggregate(Count('id'))['id__count']
