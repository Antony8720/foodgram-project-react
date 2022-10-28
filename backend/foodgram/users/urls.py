from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SubscriptionsViewSet, UserSubscribeViewSet

router = DefaultRouter()


router.register(r'users/(?P<user_id>\d+)/subscribe',
                UserSubscribeViewSet,
                basename='subscribe',)

router.register('users/subscriptions',
                SubscriptionsViewSet,
                basename='subscriptions',)

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
]
