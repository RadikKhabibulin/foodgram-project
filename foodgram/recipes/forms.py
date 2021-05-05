from .models import Recipe, Ingredient, Tag, Composition
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ('title', 'tag', 'ingredient', 'cooking_time', 'description', 'image')
        labels = {
            'title': _('Название рецепта'),
            'tag': _('Тэги'),
            'ingredient': _('Ингредиенты'),
            'cooking_time': _('Время приготовления'),
            'description': _('Описание'),
            'image': _('Загрузить фото'),
        }


class CompositionForm(ModelForm):
    class Meta:
        model = Composition
        fields = ('ingredient', 'number',)
