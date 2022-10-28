from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny

from .filters import IngredientSearchFilter, RecipeFilter
from .models import Ingredient, Recipe, Tag
from .pagination import PageNumberLimitPagination
from .permissions import OwnerOrReadOnly
from .serializers import (IngredientSerializer, RecipeSerializer,
                          RecipeSmallSerializer, RecipeWriteSerializer,
                          TagSerializer)
from .viewsets import AddingDeletingViewSet, PdfGenerateView


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (OwnerOrReadOnly,)
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    pagination_class = PageNumberLimitPagination
    filterset_class = RecipeFilter
    filterset_fields = ("tags", "author")
    ordering_fields = ("id",)

    def get_serializer_class(self):
        if self.action in (
            'create',
            'partial_update',
            'update'
        ):
            return RecipeWriteSerializer
        return RecipeSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AllowAny,)
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)
    pagination_class = None


class RecipeFavoriteViewSet(AddingDeletingViewSet):
    model_class = Recipe
    serializer_class = RecipeSmallSerializer
    router_pk = 'recipe_id'
    error_text_create = 'Рецепт уже в избранном'
    error_text_destroy = 'Такого рецепта нет в избранном'

    def is_on(self):
        recipe = self.get_object()
        return self.request.user.favorite.filter(id=recipe.id).exists()

    def perform_create(self, RecipeSmallSerializer):
        recipe = self.get_object()
        self.request.user.favorite.add(recipe)
        self.request.user.save()

    def perform_destroy(self, Recipe):
        self.request.user.favorite.remove(Recipe)
        self.request.user.save()


class RecipeCartViewSet(AddingDeletingViewSet):
    model_class = Recipe
    serializer_class = RecipeSmallSerializer
    router_pk = 'recipe_id'
    error_text_create = 'Рецепт уже добавлен в список покупок'
    error_text_destroy = 'Такого рецепта нет в списке покупок'

    def is_on(self):
        recipe = self.get_object()
        return self.request.user.cart.filter(id=recipe.id).exists()

    def perform_create(self, RecipeSmallSerializer):
        recipe = self.get_object()
        self.request.user.cart.add(recipe)
        self.request.user.save()

    def perform_destroy(self, Recipe):
        self.request.user.cart.remove(Recipe)
        self.request.user.save()


class RecipeShoppingCartDownloadView(PdfGenerateView):
    filename = 'Shopping_cart.pdf'

    def get_text_lines(self):
        recipes = self.request.user.cart.all()
        result = {}
        cart_content = recipes
        for cart_record in cart_content:
            ingredients = cart_record.ingredients.all()
            for ingredient in ingredients:
                if result.get(ingredient.ingredient):
                    result[ingredient.ingredient] += ingredient.amount
                else:
                    result[ingredient.ingredient] = ingredient.amount
        text_lines = []
        for ingredient, amount in result.items():
            text_lines.append(
                f"{ingredient.name} ({ingredient.measurement_unit}) "
                f"— {amount}"
            )

        return text_lines
