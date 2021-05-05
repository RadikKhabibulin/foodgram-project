from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Ingredient, Tag, Recipe, Composition, Follow, Favorite


# User = get_user_model()


# class UserAdmin(admin.ModelAdmin):
#     list_display = ('pk', 'username', 'email')
#     search_fields = ('username',)
#     list_filter = ('username', 'email',)
class CompositionInline(admin.TabularInline):
    model = Composition
    extra = 1


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name',)
    search_fields = ('name',)

admin.site.register(Tag, TagAdmin)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit',)
    search_fields = ('name',)
    list_filter = ('name',)

admin.site.register(Ingredient, IngredientAdmin)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author',)
    search_fields = ('title',)
    list_filter = ('title', 'author', 'tag',)
    inlines = (CompositionInline,)

admin.site.register(Recipe, RecipeAdmin)


class CompositionAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'number',)
    search_fields = ('recipe__title',)

admin.site.register(Composition, CompositionAdmin)


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author',)
    search_fields = ('author',)

admin.site.register(Follow, FollowAdmin)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    search_fields = ('user',)

admin.site.register(Favorite, FavoriteAdmin)
