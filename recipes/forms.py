from django.forms import ModelForm
from django.shortcuts import get_object_or_404
from django import forms

from .models import Composition, Recipe, Ingredient, Tag


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = (
            'title', 'tags', 'ingredients',
            'cooking_time', 'description', 'image'
        )

    def clean_ingredients(self, edit=False):
        ingredients = {}
        name_ingredient = 'nameIngredient_'
        value_ingredient = 'valueIngredient_'
        units_ingredient = 'unitsIngredient_'
        data = self.data
        for item, name in data.items():
            if name_ingredient in item:
                len_of_name = len(name_ingredient)
                unit = data.get(units_ingredient + item[len_of_name:])
                value = data.get(value_ingredient + item[len_of_name:])
                if int(value) <= 0:
                    raise forms.ValidationError(
                        'Количество ингредиента не может быть меньше 0!'
                        )
                ingredient = Ingredient.objects.filter(
                    name=name, unit=unit).exists()
                if ingredient:
                    ingredient = get_object_or_404(
                        Ingredient, name=name, unit=unit
                    )
                    ingredients[ingredient] = value
        if len(ingredients) == 0 and not edit:
            raise forms.ValidationError('Не выбраны ингредиенты!')
        return ingredients

    def clean_tags(self, edit=False):
        tags = []
        tag_slugs = ['breakfast', 'lunch', 'dinner']
        data = self.data
        for item in data:
            if item in tag_slugs:
                tag = get_object_or_404(Tag, slug=item)
                tags.append(tag)
        if len(tags) == 0 and not edit:
            raise forms.ValidationError('Не выбраны теги!')
        return tags

    def add_ingredients_and_tags(self, new_recipe):
        new_recipe.save()
        for ingredient, value in self.cleaned_data['ingredients'].items():
            composition, _ = Composition.objects.get_or_create(
                    ingredient=ingredient,
                    number=value, recipe=new_recipe
                )
            composition.save()
        for tag in self.cleaned_data['tags']:
            new_recipe.tags.add(tag)
