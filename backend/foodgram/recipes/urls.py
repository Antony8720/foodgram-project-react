from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import (RecipeViewSet, TagViewSet, IngredientViewSet,
                    RecipeFavoriteViewSet, RecipeCartViewSet,
                    RecipeShoppingCartDownloadView)

router = DefaultRouter()

router.register(r'recipes/(?P<recipe_id>\d+)/favorite',
                RecipeFavoriteViewSet,
                basename='recipe-favorite')
router.register(r'recipes/(?P<recipe_id>\d+)/shopping_cart',
                RecipeCartViewSet,
                basename='recipe-cart')
router.register('recipes', RecipeViewSet)
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)


urlpatterns = [
    path('recipes/download_shopping_cart/',
         RecipeShoppingCartDownloadView.as_view()),
    path('', include(router.urls)),
]
