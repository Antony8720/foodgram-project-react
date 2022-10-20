from rest_framework import viewsets

from .models import Recipe, Ingredient
from .serializers import RecipeWriteSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeWriteSerializer
