from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import (RecipeViewSet, TagViewSet, IngredientViewSet,
                    RecipeFavoriteViewSet, RecipeCartViewSet)

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
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
    path('', include(router.urls)),
]
