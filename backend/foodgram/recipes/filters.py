from django_filters import BaseInFilter, CharFilter
from django_filters import AllValuesMultipleFilter, NumberFilter, CharFilter
from django_filters import rest_framework as filters
from django_filters.widgets import BooleanWidget
from rest_framework.filters import SearchFilter

from .models import Recipe


class CharInFilter(BaseInFilter, CharFilter):
    pass

class IngredientSearchFilter(SearchFilter):
    search_param = 'name'


class RecipeFilter(filters.FilterSet):
    is_favorited = NumberFilter(
        field_name="users_favorited",
        method="filter_is_user_in_list",
    )
    is_in_shopping_cart = NumberFilter(
        field_name="users_added_to_cart",
        method="filter_is_user_in_list",
    )
    author = CharFilter(
        field_name="author__id",
        lookup_expr="exact",
    )
    tags = CharInFilter(
        field_name="tags__slug",
        method="filter_tags",
    )

    def filter_is_user_in_list(self, queryset, name, value):
        user = self.request.user
        if not user.is_authenticated:
            return queryset
        kwargs = {f"{name}__in": (user,)}
        if value == 0:
            return queryset.exclude(**kwargs)

        return queryset.filter(**kwargs)

    def filter_tags(self, queryset, name, value):
        tags = self.request.GET.getlist("tags")
        return queryset.filter(**{f"{name}__in": tags}).distinct()

    class Meta:
        model = Recipe
        fields = (
            "author",
            "is_favorited",
            "is_in_shopping_cart",
            "tags",
        )
