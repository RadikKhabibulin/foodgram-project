from django.urls import path

from . import views, utils

urlpatterns = [
    path('', views.index, name='index'),
    path('tag/<str:tags>/', views.index, name='index_tag'),
    path('new/', views.new_recipe, name='new_recipe'),
    path('ingredients/', utils.add_ingredient, name='add_ingredient'),
    path('follow/', views.follow_index, name='follow_index'),
    path('favorites/', views.favorites, name='favorites'),
    path('purchases/', views.purchases, name='purchases'),
    path('upload-file/', utils.upload_file, name='upload_file'),
    path(
        'favorites/tag/<str:tags>/',
        views.favorites, name='favorites_tag'
    ),
    path(
        'add-favorites/<int:recipe_id>/',
        views.add_favorites, name='add_favorites'
    ),
    path(
        'del-favorites/<int:recipe_id>/',
        views.del_favorites, name='del_favorites'
    ),
    path(
        'add-purchases/<int:recipe_id>/',
        views.add_purchases, name='add_purchases'
    ),
    path(
        'del-purchases/<int:recipe_id>/',
        views.del_purchases, name='del_purchases'
    ),
    path('profile/<str:username>/', views.profile, name='profile'),
    path(
        'profile/<str:username>/tag/<str:tags>/',
        views.profile, name='profile_tag'
    ),
    path(
        'follow/<str:username>/',
        views.profile_follow, name='profile_follow'
    ),
    path(
        'unfollow/<str:username>/',
        views.profile_unfollow, name='profile_unfollow'
    ),
    path('<str:username>/<int:recipe_id>/', views.recipe_view, name='recipe'),
    path(
        '<str:username>/<int:recipe_id>/edit/',
        views.recipe_edit, name='recipe_edit'
    ),
    path(
        '<str:username>/<int:recipe_id>/del/',
        views.recipe_del, name='recipe_del'
    ),
]
