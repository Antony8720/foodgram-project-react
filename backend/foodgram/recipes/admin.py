from django.contrib import admin
from django.db.models import Count

from .models import Ingredient, Recipe,  Tag


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author', 'name',)
    list_filter = ('author', 'name', 'tags',)
    readonly_fields = ("favorited",)

    def favorited(self, Recipe):
        return Recipe.users_favorited.aggregate(Count("id"))["id__count"]

    favorited.short_description = "Общее число добавлений рецепта в избранное"


class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
