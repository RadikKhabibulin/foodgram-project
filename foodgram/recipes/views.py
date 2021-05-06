from django.http import JsonResponse, HttpResponse
from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
    get_list_or_404,
)
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .forms import RecipeForm
from .models import (
    Ingredient, Tag, Recipe, User,
    Composition, Follow, Favorite, Purchase
)


def index(request):
    user = request.user
    recipe_list = Recipe.objects.all()
    param_dict = get_param_dict(recipe_list, user)
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    purchases_count = get_purchases_count(user)
    return render(request, 'index.html', {
            'page': page, 'param_dict': param_dict,
            'paginator': paginator, 'purchases_count': purchases_count,
        }
    )


def index_tag(request, tags):
    if tags == 'empty':
        return redirect('index')
    user = request.user
    tags = tags.split('+')
    recipe_list = Recipe.objects.filter(tag__slug__in=tags).distinct()
    param_dict = get_param_dict(recipe_list, user)
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    tags = '+'.join(tags)
    purchases_count = get_purchases_count(user)
    return render(request, 'index.html', {
            'page': page, 'param_dict': param_dict,
            'paginator': paginator, 'tags': tags,
            'purchases_count': purchases_count
        }
    )


def recipe_view(request, username, recipe_id):
    user = request.user
    recipe = get_object_or_404(
        Recipe,
        id=recipe_id,
        author_id__username=username
    )
    tags = recipe.tag.all()
    ingredients = get_list_or_404(Composition, recipe=recipe)
    author = get_object_or_404(User, username=username)
    if user.is_authenticated:
        following = Follow.objects.filter(user=user, author=author).exists()
        favorites = Favorite.objects.filter(user=user, recipe=recipe).exists()
        purchases = Purchase.objects.filter(user=user, recipe=recipe).exists()
        purchases_count = Purchase.objects.filter(user=user).count()
        return render(request, 'recipe.html', {
                'recipe': recipe, 'tags': tags,
                'ingredients': ingredients, 'following': following,
                'favorites': favorites, 'purchases': purchases,
                'purchases_count': purchases_count
            }
        )
    return render(request, 'recipe.html', {
            'recipe': recipe, 'tags': tags,
            'ingredients': ingredients,
        }
    )


def profile(request, username):
    user = request.user
    profile = get_object_or_404(User, username=username)
    recipe_list = profile.recipes.all()
    param_dict = get_param_dict(recipe_list, user)
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    recipes_count = profile.recipes.count()
    following = (
        user.is_authenticated and
        Follow.objects.filter(user=user, author=profile).exists()
    )
    purchases_count = get_purchases_count(user)

    return render(request, 'profile.html', {
            'profile': profile, 'page': page,
            'paginator': paginator, 'param_dict': param_dict,
            'username': username, 'recipes_count': recipes_count,
            'following': following, 'purchases_count': purchases_count
        }
    )


def profile_tag(request, username, tags):
    if tags == 'empty':
        return redirect('profile', username=username)
    user = request.user
    tags = tags.split('+')
    profile = get_object_or_404(User, username=username)
    recipe_list = Recipe.objects.filter(
        tag__slug__in=tags, author=profile).distinct()
    param_dict = get_param_dict(recipe_list, user)
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    recipes_count = profile.recipes.count()
    purchases_count = get_purchases_count(user)
    following = (
        user.is_authenticated and
        Follow.objects.filter(user=user, author=profile).exists()
    )
    tags = '+'.join(tags)
    return render(request, 'profile.html', {
            'profile': profile, 'page': page,
            'paginator': paginator, 'param_dict': param_dict,
            'tags': tags, 'username': username,
            'recipes_count': recipes_count, 'following': following,
            'purchases_count': purchases_count,
        }
    )


@login_required
def new_recipe(request):
    user = request.user
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    purchases_count = Purchase.objects.filter(user=user).count()
    if form.is_valid():
        new_recipe = form.save(commit=False)
        new_recipe.author = user
        new_compositions, new_tags = request_parsing(new_recipe, request)
        errors = []
        if len(new_tags) == 0:
            errors.append('Не выбраны теги!')
        if len(new_compositions) == 0:
            errors.append('Не выбраны ингредиенты!')
        if len(errors) > 0:
            return render(
                request, 'new_recipe.html', {
                    'form': form, 'compositions': new_compositions,
                    'tags': new_tags, 'errors': errors,
                    'purchases_count': purchases_count,
                }
            )
        new_recipe.save()
        for composition in new_compositions:
            composition.save()
        for tag in new_tags:
            new_recipe.tag.add(tag)
        return redirect('index')
    return render(request, 'new_recipe.html', {
            'form': form, 'purchases_count': purchases_count,
        }
    )


@login_required
def recipe_edit(request, username, recipe_id):
    user = request.user
    purchases_count = Purchase.objects.filter(user=user).count()
    editable_recipe = get_object_or_404(
        Recipe, id=recipe_id, author_id__username=username
    )
    compositions = get_list_or_404(
        Composition, recipe__id=editable_recipe.id
    )
    tags = editable_recipe.tag.all()
    if user != editable_recipe.author:
        return recipe_view(request, username, recipe_id)
    form = RecipeForm(
        request.POST or None, files=request.FILES or None,
        instance=editable_recipe
    )
    if form.is_valid():
        new_recipe = form.save(commit=False)
        new_compositions, new_tags = request_parsing(
            new_recipe, request, edit=True)
        errors = []
        if len(new_tags) == 0:
            errors.append('Не выбраны теги!')
        if len(new_compositions) == 0:
            errors.append('Не выбраны ингредиенты!')
        if len(errors) > 0:
            return render(request, 'new_recipe.html', {
                    'form': form, 'compositions': new_compositions,
                    'tags': new_tags, 'errors': errors,
                    'purchases_count': purchases_count,
                }
            )
        new_recipe.save()
        new_recipe.tag.clear()
        for composition in compositions:
            composition.delete()
        for composition in new_compositions:
            composition.save()
        for tag in new_tags:
            new_recipe.tag.add(tag)
        return redirect('recipe', username=username, recipe_id=recipe_id)
    return render(request, 'new_recipe.html', {
            'form': form, 'recipe_id': recipe_id,
            'username': username, 'recipe': editable_recipe,
            'compositions': compositions, 'tags': tags,
            'purchases_count': purchases_count,
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
    purchases_count = Purchase.objects.filter(user=user).count()
    following = Follow.objects.filter(user=user)
    recipe_dict = {}
    for follow in following:
        recipes_count = follow.author.recipes.count()
        recipe_list = []
        for recipe in follow.author.recipes.all()[:3]:
            recipe_list.append(recipe)
        if recipes_count > 3:
            if (recipes_count - 3) == 1:
                recipe_list.append(str(recipes_count - 3) + ' рецепт')
            elif 1 < (recipes_count - 3) < 5:
                recipe_list.append(str(recipes_count - 3) + ' рецепта')
            else:
                recipe_list.append(str(recipes_count - 3) + ' рецептов')
        recipe_dict[follow.author] = recipe_list
    paginator = Paginator(following, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'follow.html', {
            'page': page, 'paginator': paginator,
            'recipe_dict': recipe_dict, 'purchases_count': purchases_count,
        }
    )


@login_required
def profile_follow(request, username):
    user = request.user
    author = get_object_or_404(User, username=username)
    following = Follow.objects.filter(user=user, author=author).exists()
    if user != author and following is False:
        Follow.objects.create(user=user, author=author)
        return JsonResponse({'success': 'true'}, safe=False)
    return JsonResponse({'success': 'false'}, safe=False)


@login_required
def profile_unfollow(request, username):
    user = request.user
    author = get_object_or_404(User, username=username)
    if Follow.objects.filter(user=user, author=author).exists():
        unfollow = Follow.objects.filter(user=user, author=author)
        unfollow.delete()
        return JsonResponse({'success': 'true'}, safe=False)
    return JsonResponse({'success': 'false'}, safe=False)


@login_required
def add_favorites(request, recipe_id):
    user = request.user
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if Favorite.objects.filter(user=user, recipe=recipe).exists() is False:
        Favorite.objects.create(user=user, recipe=recipe)
        return JsonResponse({'success': 'true'}, safe=False)
    return JsonResponse({'success': 'false'}, safe=False)


@login_required
def del_favorites(request, recipe_id):
    user = request.user
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if Favorite.objects.filter(user=user, recipe=recipe).exists():
        del_favorite = Favorite.objects.filter(user=user, recipe=recipe)
        del_favorite.delete()
        return JsonResponse({'success': 'true'}, safe=False)
    return JsonResponse({'success': 'false'}, safe=False)


@login_required
def favorites(request):
    user = request.user
    favorites = user.reader.all()
    recipes = [item.recipe for item in favorites]
    recipes.reverse()
    param_dict = get_param_dict(recipes, user)
    purchases_count = Purchase.objects.filter(user=user).count()
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'favorites.html', {
            'page': page, 'paginator': paginator,
            'param_dict': param_dict, 'purchases_count': purchases_count,
        }
    )


@login_required
def favorites_tag(request, tags):
    if tags == 'empty':
        return redirect('favorites')
    user = request.user
    tags = tags.split('+')
    favorites = user.reader.all()
    recipes = []
    for item in favorites:
        for elem in item.recipe.tag.all():
            if elem.slug in tags and item.recipe not in recipes:
                recipes.append(item.recipe)
    recipes.reverse()
    param_dict = get_param_dict(recipes, user)
    purchases_count = Purchase.objects.filter(user=user).count()
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    tags = '+'.join(tags)
    return render(request, 'favorites.html', {
            'page': page, 'paginator': paginator,
            'param_dict': param_dict, 'tags': tags,
            'purchases_count': purchases_count,
        }
    )


@login_required
def purchases(request):
    user = request.user
    purchases = user.buyer.all()
    recipes = [item.recipe for item in purchases]
    purchases_count = Purchase.objects.filter(user=user).count()
    return render(request, 'shop_list.html', {
            'recipes': recipes, 'purchases_count': purchases_count,
        }
    )


@login_required
def add_purchases(request, recipe_id):
    user = request.user
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if Purchase.objects.filter(user=user, recipe=recipe).exists() is False:
        Purchase.objects.create(user=user, recipe=recipe)
        return JsonResponse({'success': 'true'}, safe=False)
    return JsonResponse({'success': 'false'}, safe=False)


@login_required
def del_purchases(request, recipe_id):
    user = request.user
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if Purchase.objects.filter(user=user, recipe=recipe).exists():
        del_purchase = Purchase.objects.filter(user=user, recipe=recipe)
        del_purchase.delete()
        return JsonResponse({'success': 'true'}, safe=False)
    return JsonResponse({'success': 'false'}, safe=False)


def request_parsing(new_recipe, request, edit=False):
    variables = request.POST
    name_ingredient = 'nameIngredient_'
    value_ingredient = 'valueIngredient_'
    units_ingredient = 'unitsIngredient_'
    tag_slugs = ['breakfast', 'lunch', 'dinner']
    new_tags = []
    new_compositions = []
    for item in variables:
        if name_ingredient in item:
            name = request.POST.get(
                name_ingredient + item[len(name_ingredient):]
            )
            unit = request.POST.get(
                units_ingredient + item[len(name_ingredient):]
            )
            value = request.POST.get(
                value_ingredient + item[len(name_ingredient):]
            )
            ingredient = get_object_or_404(
                Ingredient, name=name, unit=unit)
            if edit:
                composition, created = Composition.objects.get_or_create(
                    ingredient=ingredient,
                    number=value, recipe=new_recipe
                )
            else:
                composition = Composition(
                    ingredient=ingredient,
                    number=value, recipe=new_recipe
                )
            new_compositions.append(composition)
        if item in tag_slugs:
            new_tag = get_object_or_404(Tag, slug=item)
            new_tags.append(new_tag)
    return new_compositions, new_tags


def add_ingredient(request):
    ingredients = get_list_or_404(Ingredient)
    search_name = request.GET.get('query')
    data = []
    # if search_name != '':
    #     for item in ingredients:
    #         if search_name.lower() in item.name.lower():
    #             ingredient = {'title': item.name, 'dimension': item.unit}
    #             data.append(ingredient)
    for item in ingredients:
        if search_name.lower() in item.name.lower():
            ingredient = {'title': item.name, 'dimension': item.unit}
            data.append(ingredient)
    # if len(data) == 0:
    #     data = [{'title': 'Ингредиент не найден', 'dimension': 'шт'}]
    return JsonResponse(data, safe=False)


def get_purchases_count(user):
    if user.is_authenticated:
        purchases_count = Purchase.objects.filter(user=user).count()
    else:
        purchases_count = False
    return purchases_count


def get_param_dict(recipes, user):
    param_dict = {}
    for recipe in recipes:
        param_list = []
        for tag in recipe.tag.all():
            param_list.append(tag.name)
        if user.is_authenticated:
            if Favorite.objects.filter(recipe=recipe, user=user).exists():
                param_list.append('del-favorites')
            else:
                param_list.append('add-favorites')
            if Purchase.objects.filter(recipe=recipe, user=user).exists():
                param_list.append('del-purchases')
            else:
                param_list.append('add-purchases')
        param_dict[recipe.id] = param_list
    return param_dict


def upload_file(request):
    user = request.user
    purchases = user.buyer.all()
    recipes = [item.recipe for item in purchases]
    filename = ('shop_lists/' + user.username + '.txt')
    shop_file = open(filename, 'w')
    shop_list = {}
    for recipe in recipes:
        compositions = Composition.objects.filter(recipe=recipe)
        for item in compositions:
            title = (item.ingredient.name + ' (' + item.ingredient.unit + ')')
            number = item.number
            if (title) in shop_list.keys():
                shop_list[title] = shop_list[title] + number
            else:
                shop_list[title] = number
    for title, number in shop_list.items():
        shop_file.write(' - ' + title + ': ' + str(number) + '\n')
    shop_file.close()
    response = HttpResponse(open(filename), content_type='application/txt')
    response['Content-Disposition'] = 'attachment; filename="shoplist.txt"'
    return response
