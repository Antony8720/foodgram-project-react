from rest_framework.routers import DefaultRouter

from django.urls import include, path

from recipes.views import RecipeViewSet

router = DefaultRouter()

router.register('recipes', RecipeViewSet)


urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
    path('', include(router.urls)),
]
