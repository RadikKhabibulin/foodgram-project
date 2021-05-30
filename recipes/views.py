from recipes.utils import recipes_by_tag
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import (get_list_or_404, get_object_or_404, redirect,
                              render)
from django.contrib.sites.shortcuts import get_current_site

from foodgram.settings import PAGE_SIZE
from .forms import RecipeForm
from .models import Composition, Favorite, Follow, Purchase, Recipe, User


def index(request, tags='empty'):
    recipes = Recipe.objects.all()
    if tags != 'empty':
        recipes = recipes_by_tag(tags, recipes)
    paginator = Paginator(recipes, PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    domain = get_current_site(request)
    return render(request, 'index.html', {
            'domain': domain,
            'page': page,
            'tags': tags, 'paginator': paginator,
        }
    )


def recipe_view(request, username, recipe_id):
    recipe = get_object_or_404(
        Recipe, id=recipe_id,
        author_id__username=username
    )
    ingredients = get_list_or_404(Composition, recipe=recipe)
    return render(request, 'recipe.html', {
            'recipe': recipe, 'ingredients': ingredients,
        }
    )


def profile(request, username, tags='empty'):
    profile = get_object_or_404(User, username=username)
    recipes = profile.recipes.all()
    if tags != 'empty':
        recipes = recipes_by_tag(tags, recipes)
    paginator = Paginator(recipes, PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    recipes_count = profile.recipes.count()
    return render(request, 'profile.html', {
            'profile': profile, 'page': page,
            'paginator': paginator, 'tags': tags,
            'recipes_count': recipes_count,
        }
    )


@login_required
def new_recipe(request):
    user = request.user
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        new_recipe = form.save(commit=False)
        new_recipe.author = user
        form.add_ingredients_and_tags(new_recipe)
        return redirect('index')
    tags = []
    compositions = {}
    if request.method == 'POST':
        if not form['tags'].errors:
            tags = form.clean_tags(edit=True)
        if not form['ingredients'].errors:
            compositions = form.clean_ingredients(edit=True)
    return render(request, 'new_recipe.html', {
            'form': form, 'tags': tags, 'compositions': compositions
        }
    )


@login_required
def recipe_edit(request, username, recipe_id):
    user = request.user
    editable_recipe = get_object_or_404(
        Recipe, id=recipe_id, author_id__username=username
    )
    compositions = {}
    compositions_list = get_list_or_404(
        Composition, recipe__id=editable_recipe.id
    )
    for obj in compositions_list:
        compositions[obj.ingredient] = obj.number
    tags = editable_recipe.tags.all()
    if user != editable_recipe.author:
        return recipe_view(request, username, recipe_id)
    form = RecipeForm(
        request.POST or None, files=request.FILES or None,
        instance=editable_recipe
    )
    file_url = None
    if form.initial['image']:
        file_url = form.initial['image'].url
    if form.is_valid():
        new_recipe = form.save(commit=False)
        new_recipe.tags.clear()
        for composition in compositions_list:
            composition.delete()
        form.add_ingredients_and_tags(new_recipe)
        return redirect('recipe', username=username, recipe_id=recipe_id)
    return render(request, 'new_recipe.html', {
            'form': form, 'recipe_id': recipe_id,
            'username': username, 'recipe': editable_recipe,
            'compositions': compositions, 'tags': tags,
            'file_url': file_url,
        }
    )


@login_required
def recipe_del(request, username, recipe_id):
    recipe_to_delete = get_object_or_404(
        Recipe, id=recipe_id, author_id__username=username)
    if request.user != recipe_to_delete.author:
        return recipe_view(request, username, recipe_id)
    recipe_to_delete.delete()
    return redirect('index')


@login_required
def follow_index(request):
    user = request.user
    following = Follow.objects.filter(user=user)
    recipe_dict = {}
    for follow in following:
        recipes_count = follow.author.recipes.count()
        recipe_list = []
        for recipe in follow.author.recipes.all()[:3]:
            recipe_list.append(recipe)
        if recipes_count > 3:
            new_count = recipes_count - 3
            if (new_count % 10) == 1:
                recipe_list.append(str(new_count) + ' рецепт')
            elif 1 < (new_count % 10) < 5:
                recipe_list.append(str(new_count) + ' рецепта')
            else:
                recipe_list.append(str(new_count) + ' рецептов')
        recipe_dict[follow.author] = recipe_list
    paginator = Paginator(following, PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'follow.html', {
            'page': page, 'paginator': paginator,
            'recipe_dict': recipe_dict,
        }
    )


@login_required
def profile_follow(request, username):
    user = request.user
    author = get_object_or_404(User, username=username)
    if user != author:
        _, created = Follow.objects.get_or_create(user=user, author=author)
        return JsonResponse({'success': created}, safe=False)
    return JsonResponse({'success': False}, safe=False)


@login_required
def profile_unfollow(request, username):
    user = request.user
    author = get_object_or_404(User, username=username)
    _, deleted = Follow.objects.filter(user=user, author=author).delete()
    if deleted:
        return JsonResponse({'success': True}, safe=False)
    return JsonResponse({'success': False}, safe=False)


@login_required
def add_favorites(request, recipe_id):
    user = request.user
    recipe = get_object_or_404(Recipe, id=recipe_id)
    _, created = Favorite.objects.get_or_create(user=user, recipe=recipe)
    return JsonResponse({'success': created}, safe=False)


@login_required
def del_favorites(request, recipe_id):
    user = request.user
    recipe = get_object_or_404(Recipe, id=recipe_id)
    _, deleted = Favorite.objects.filter(user=user, recipe=recipe).delete()
    if deleted:
        return JsonResponse({'success': True}, safe=False)
    return JsonResponse({'success': False}, safe=False)


@login_required
def favorites(request, tags='empty'):
    user = request.user
    favorites = user.reader.all()
    recipes_id = list(favorites.values_list('recipe', flat=True))
    recipes = Recipe.objects.filter(id__in=recipes_id).distinct()
    if tags != 'empty':
        recipes = recipes_by_tag(tags, recipes)
    paginator = Paginator(recipes, PAGE_SIZE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'favorites.html', {
            'page': page, 'paginator': paginator, 'tags': tags,
        }
    )


@login_required
def purchases(request):
    user = request.user
    purchases = user.buyer.all()
    recipes_id = list(purchases.values_list('recipe', flat=True))
    recipes = Recipe.objects.filter(id__in=recipes_id).distinct()
    return render(request, 'shop_list.html', {'recipes': recipes})


@login_required
def add_purchases(request, recipe_id):
    user = request.user
    recipe = get_object_or_404(Recipe, id=recipe_id)
    _, created = Purchase.objects.get_or_create(user=user, recipe=recipe)
    return JsonResponse({'success': created}, safe=False)


@login_required
def del_purchases(request, recipe_id):
    user = request.user
    recipe = get_object_or_404(Recipe, id=recipe_id)
    _, deleted = Purchase.objects.filter(user=user, recipe=recipe).delete()
    if deleted:
        return JsonResponse({'success': True}, safe=False)
    return JsonResponse({'success': False}, safe=False)
