from rest_framework import serializers
from .models import User
from djoser.serializers import UserCreateSerializer, UserSerializer


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
