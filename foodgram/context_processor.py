from recipes.models import Purchase


def purchases_count(request):
    purchases_count = Purchase.objects.filter(user=request.user).count()
    return {
        'purchases_count': purchases_count
    }
