from recipes.models import Purchase


def purchases_count(request):
    purchases_count = 0
    if request.user.is_authenticated:
        purchases_count = Purchase.objects.filter(user=request.user).count()
    return {
        'purchases_count': purchases_count
    }
