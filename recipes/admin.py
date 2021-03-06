from django.contrib import admin

from .models import (Composition, Favorite, Follow, Ingredient, Purchase,
                     Recipe, Tag)


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
    list_filter = ('unit',)


admin.site.register(Ingredient, IngredientAdmin)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author',)
    search_fields = ('title',)
    list_filter = ('title', 'author', 'tags',)
    inlines = (CompositionInline,)


admin.site.register(Recipe, RecipeAdmin)


class CompositionAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'number',)
    search_fields = ('ingredient__name',)
    list_filter = ('recipe__title',)


admin.site.register(Composition, CompositionAdmin)


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author',)
    search_fields = ('user__username',)
    list_filter = ('author',)


admin.site.register(Follow, FollowAdmin)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    search_fields = ('recipe__title',)
    list_filter = ('user',)


admin.site.register(Favorite, FavoriteAdmin)


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    search_fields = ('user',)


admin.site.register(Purchase, PurchaseAdmin)
