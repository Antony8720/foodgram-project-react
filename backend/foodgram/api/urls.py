from rest_framework.routers import DefaultRouter

from django.urls import include, path


router = DefaultRouter()


urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')), 
]
