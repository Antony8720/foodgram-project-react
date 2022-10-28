from django.contrib import admin

from .models import Ingredient, Recipe,  Tag


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author', 'name', 'recipe_count')
    list_filter = ('author', 'name', 'tags')


admin.site.register(Recipe)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag)
