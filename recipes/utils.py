from django.http import HttpResponse, JsonResponse

from .models import Composition, Ingredient


def add_ingredient(request):
    search_name = request.GET.get('query')
    data = list(
        Ingredient.objects.filter(
            name__icontains=search_name).values('name', 'unit')
    )
    if len(data) == 0:
        data = list(Ingredient.objects.values('name', 'unit'))
    return JsonResponse(data, safe=False)


def upload_file(request):
    user = request.user
    purchases = user.buyer.all()
    recipes_id = purchases.values_list('recipe', flat=True)
    shop_dict = {}
    for id in recipes_id:
        compositions = Composition.objects.filter(recipe__id=id)
        for item in compositions:
            title = (item.ingredient.name + ' (' + item.ingredient.unit + ')')
            number = item.number
            if title in shop_dict:
                shop_dict[title] = shop_dict[title] + number
            else:
                shop_dict[title] = number
    shop_file = []
    for title, number in shop_dict.items():
        shop_file.append(' - ' + title + ': ' + str(number) + '\n')
    response = HttpResponse(shop_file, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="shoplist.txt"'
    return response


def recipes_by_tag(tags, recipes):
    tags = tags.split('+')
    return recipes.filter(tags__slug__in=tags).distinct()
