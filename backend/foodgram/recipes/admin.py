from django.contrib import admin
from .models import Recipe, Ingredient, Tag


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'maesurement_init')
    list_filter = ('name',)


admin.site.register(Recipe)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag)
