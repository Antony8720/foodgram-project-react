from recipes.mixins import ListModelViewSet
from recipes.pagination import PageNumberLimitPagination
from recipes.viewsets import AddingDeletingViewSet
from rest_framework import permissions

from .models import User
from .serializers import UserSubscribeSerializer


class UserSubscribeViewSet(AddingDeletingViewSet):
    model_class = User
    serializer_class = UserSubscribeSerializer
    router_pk = 'user_id'
    error_text_create = 'Подписка уже существует'
    error_text_destroy = 'Подписки не существует'

    def is_on(self):
        recipe = self.get_object()
        return self.request.user.follower.filter(id=recipe.id).exists()

    def create(self, request, *args, **kwargs):
        user = self.get_object()
        if self.request.user.id == user.id:
            return self.error('Невозможно подписаться на самого себя')
        return super().create(request, *args, **kwargs)

    def perform_create(self, RecipeSmallSerializer):
        recipe = self.get_object()
        self.request.user.follower.add(recipe)
        self.request.user.save()

    def perform_destroy(self, Recipe):
        self.request.user.follower.remove(Recipe)
        self.request.user.save()


class SubscriptionsViewSet(ListModelViewSet):
    serializer_class = UserSubscribeSerializer
    permissions_classes = (permissions.IsAuthenticated,)
    pagination_class = PageNumberLimitPagination

    def get_queryset(self):
        return self.request.user.follower.all()
