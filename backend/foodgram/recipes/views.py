from rest_framework import viewsets

from .models import Recipe
from .serializers import RecipeWriteSerializer, RecipeSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    
    def get_serializer_class(self):
        if self.action in (
            'create',
            'partial_update',
            'update'
        ):
            return RecipeWriteSerializer
        return RecipeSerializer
