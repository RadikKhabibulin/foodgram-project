from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tag/<str:tags>/', views.index_tag, name='index_tag'),
    path('new/', views.new_recipe, name='new_recipe'),
    path('ingredients/', views.add_ingredient, name='add_ingredient'),
    path('follow/', views.follow_index, name='follow_index'),
    path('favorites/', views.favorites, name='favorites'),
    path('purchases/', views.purchases, name='purchases'),
    path('upload-file/', views.upload_file, name='upload_file'),
    path(
        'favorites/tag/<str:tags>/',
        views.favorites_tag, name='favorites_tag'
    ),
    path(
        '<int:recipe_id>/add-favorites/',
        views.add_favorites, name='add_favorites'
    ),
    path(
        '<int:recipe_id>/del-favorites/',
        views.del_favorites, name='del_favorites'
    ),
    path(
        '<int:recipe_id>/add-purchases/',
        views.add_purchases, name='add_purchases'
    ),
    path(
        '<int:recipe_id>/del-purchases/',
        views.del_purchases, name='del_purchases'
    ),
    path('<str:username>/', views.profile, name='profile'),
    path(
        '<str:username>/tag/<str:tags>/',
        views.profile_tag, name='profile_tag'
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
    path(
        '<str:username>/follow/',
        views.profile_follow, name='profile_follow'
    ),
    path(
        '<str:username>/unfollow/',
        views.profile_unfollow, name='profile_unfollow'
    ),
    
]
