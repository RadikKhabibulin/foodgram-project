import json
from django.http import JsonResponse
from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
    get_list_or_404,
)
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .forms import RecipeForm, CompositionForm
from .models import Ingredient, Tag, Recipe, User, Composition, Follow, Favorite


def index(request):
    recipe_list = Recipe.objects.all()
    tag_dict = {}
    for recipe in recipe_list:
        tag_list = []
        for tag in recipe.tag.all():
            tag_list.append(tag.name)
        if request.user.is_authenticated:
            if Favorite.objects.filter(recipe=recipe, user=request.user).exists():
                tag_list.append('del-favorites')
            else:
                tag_list.append('add-favorites')
        tag_dict[recipe.id] = tag_list
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        'index.html',
        {'page': page, 'tag_dict': tag_dict, 'paginator': paginator}
   )


def index_tag(request, tag):
    recipe_list = Recipe.objects.filter(tag__slug=tag)
    tag_dict = {}
    for recipe in recipe_list:
        tag_list = []
        for tag in recipe.tag.all():
            tag_list.append(tag.name)
        if request.user.is_authenticated:
            if Favorite.objects.filter(recipe=recipe, user=request.user).exists():
                tag_list.append('del-favorites')
            else:
                tag_list.append('add-favorites')
        tag_dict[recipe.id] = tag_list
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        'index.html',
        {'page': page, 'tag_dict': tag_dict, 'paginator': paginator, 'tag': tag}
   )


def recipe_view(request, username, recipe_id):
    recipe = get_object_or_404(
        Recipe,
        id=recipe_id,
        author_id__username=username
    )
    tags = recipe.tag.all()
    ingredients = get_list_or_404(Composition, recipe=recipe)
    author = get_object_or_404(User, username=username)
    following = request.user.is_authenticated and Follow.objects.filter(user=request.user, author=author).exists()
    favorites = request.user.is_authenticated and Favorite.objects.filter(user=request.user, recipe=recipe).exists()
    return render(
        request,
        'recipe.html',
        {'recipe': recipe, 'tags': tags, 'ingredients': ingredients, 'following': following, 'favorites': favorites}
    )


def profile(request, username):
    profile = get_object_or_404(User, username=username) 
    recipe_list = profile.recipes.all()
    tag_dict = {}
    for recipe in recipe_list:
        tag_list = []
        for tag in recipe.tag.all():
            tag_list.append(tag.name)
        if request.user.is_authenticated:
            if Favorite.objects.filter(recipe=recipe, user=request.user).exists():
                tag_list.append('del-favorites')
            else:
                tag_list.append('add-favorites')
        tag_dict[recipe.id] = tag_list
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    recipes_count = profile.recipes.count()
    # followers_list = profile.following.all()
    # count_of_followers = followers_list.count()
    # count_of_followings = profile.follower.all().count()
    following = request.user.is_authenticated and Follow.objects.filter(user=request.user, author=profile).exists()

    return render(
                    request, 
                    'profile.html', {
                    'profile':profile,
                    'page':page,
                    'paginator':paginator,
                    'tag_dict':tag_dict,
                    'username':username,
                    'recipes_count':recipes_count,
                    'following':following,
                    # 'count_of_followings':count_of_followings,
                    # 'count_of_followers':count_of_followers,
                    }
                )


def profile_tag(request, username, tag):
    profile = get_object_or_404(User, username=username)
    recipe_list = Recipe.objects.filter(tag__slug=tag, author=profile)
    tag_dict = {}
    for recipe in recipe_list:
        tag_list = []
        for tag in recipe.tag.all():
            tag_list.append(tag.name)
        if request.user.is_authenticated:
            if Favorite.objects.filter(recipe=recipe, user=request.user).exists():
                tag_list.append('del-favorites')
            else:
                tag_list.append('add-favorites')
        tag_dict[recipe.id] = tag_list
    paginator = Paginator(recipe_list, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    recipes_count = profile.recipes.count()
    # followers_list = profile.following.all()
    # count_of_followers = followers_list.count()
    # count_of_followings = profile.follower.all().count()
    following = request.user.is_authenticated and Follow.objects.filter(user=request.user, author=profile).exists()

    return render(
                    request, 
                    'profile.html', {
                    'profile':profile,
                    'page':page,
                    'paginator':paginator,
                    'tag_dict':tag_dict,
                    'tag':tag,
                    'username':username,
                    'recipes_count':recipes_count,
                    'following':following,
                    # 'count_of_followings':count_of_followings,
                    # 'count_of_followers':count_of_followers,
                    }
                )


def request_parsing(new_recipe, request, edit=False):
    variables = request.POST
    name_ingredient = 'nameIngredient_'
    value_ingredient = 'valueIngredient_'
    units_ingredient = 'unitsIngredient_'
    tag_slugs = ['breakfast', 'lunch', 'dinner']
    errors = []
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
                    number=value, recipe=new_recipe)
            else:
                composition = Composition(
                    ingredient=ingredient,
                    number=value, recipe=new_recipe)
            new_compositions.append(composition)
        if item in tag_slugs:
            new_tag = get_object_or_404(Tag, slug=item)
            new_tags.append(new_tag)    
    return new_compositions, new_tags


@login_required
def new_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        new_recipe = form.save(commit=False)
        new_recipe.author = request.user
        new_compositions, new_tags = request_parsing(new_recipe, request)
        errors = []
        if len(new_tags) == 0:
            errors.append('Не выбраны теги!')
        if len(new_compositions) == 0:
            errors.append('Не выбраны ингредиенты!')
        if len(errors) > 0:
            return render(
                request,
                'new_recipe.html',
                {'form': form, 'compositions':new_compositions, 'tags':new_tags,  'errors': errors}
            )
        new_recipe.save()
        for composition in new_compositions:
            composition.save()
        for tag in new_tags:
            new_recipe.tag.add(tag)
        return redirect('index')
    return render(request, 'new_recipe.html', {'form':form})


@login_required
def recipe_edit(request, username, recipe_id):
    editable_recipe = get_object_or_404(Recipe, id=recipe_id, author_id__username=username)
    compositions = get_list_or_404(Composition, recipe__id = editable_recipe.id)
    tags = editable_recipe.tag.all()
    if request.user != editable_recipe.author:
        return recipe_view(request, username, recipe_id)

    form = RecipeForm(request.POST or None, files=request.FILES or None, instance=editable_recipe)
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
            return render(
                request,
                'new_recipe.html',
                {'form': form,
                'compositions':new_compositions,
                'tags':new_tags, 
                'errors': errors}
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
    return render(
        request,
        'new_recipe.html', 
        {'form':form,
        'recipe_id':recipe_id,
        'username':username,
        'recipe':editable_recipe,
        'compositions':compositions,
        'tags':tags}
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
    following = Follow.objects.filter(user=request.user)
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
    return render(request, 'follow.html', {'page': page, 'paginator': paginator, 'recipe_dict': recipe_dict})


@login_required
def profile_follow(request, username):
    user = request.user
    author = get_object_or_404(User, username=username)

    if user != author and Follow.objects.filter(user=user, author=author).exists() == False:
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

    if Favorite.objects.filter(user=user, recipe=recipe).exists() == False:
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
    favorites = request.user.reader.all()
    recipes = []
    tag_dict = {}
    for item in favorites:
        recipes.append(item.recipe)
    for recipe in recipes:
        tag_list = []
        for tag in recipe.tag.all():
            tag_list.append(tag.name)
        if request.user.is_authenticated:
            if Favorite.objects.filter(recipe=recipe, user=request.user).exists():
                tag_list.append('del-favorites')
            else:
                tag_list.append('add-favorites')
        tag_dict[recipe.id] = tag_list
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'favorites.html', {'page': page, 'paginator': paginator, 'tag_dict': tag_dict})
    return redirect('favorites')


@login_required
def favorites_tag(request, tag):
    print(tag)
    favorites = request.user.reader.all()
    recipes = []
    tag_dict = {}
    for item in favorites:
        for elem in item.recipe.tag.all():
            if elem.slug == tag:
                recipes.append(item.recipe)
    for recipe in recipes:
        tag_list = []
        for tagy in recipe.tag.all():
            tag_list.append(tagy.name)
        if request.user.is_authenticated:
            if Favorite.objects.filter(recipe=recipe, user=request.user).exists():
                tag_list.append('del-favorites')
            else:
                tag_list.append('add-favorites')
        tag_dict[recipe.id] = tag_list
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    print(tag)
    return render(request, 'favorites.html', {'page': page, 'paginator': paginator, 'tag_dict': tag_dict, 'tag': tag})


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
