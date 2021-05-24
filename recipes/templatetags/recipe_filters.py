from django import template

from recipes.models import Favorite, Follow, Purchase

register = template.Library()


@register.filter
def del_tag(tags, tag):
    tags = tags.split('+')
    tags = list(set(tags))
    if tag in tags:
        tags.remove(tag)
    tags = '+'.join(tags)
    if len(tags) == 0:
        tags = 'empty'
    return tags


@register.filter
def get_purchases(user, recipe):
    return Purchase.objects.filter(user=user, recipe=recipe).exists()


@register.filter
def get_favorites(user, recipe):
    return Favorite.objects.filter(user=user, recipe=recipe).exists()


@register.filter
def get_following(user, author):
    return Follow.objects.filter(user=user, author=author).exists()


@register.filter
def recipe_tags(recipe):
    recipe_tags = list(recipe.tags.values_list('name', flat=True))
    return recipe_tags
