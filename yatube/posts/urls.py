from django.urls import path
from . import views

app_name = 'posts'  # Добавляем namespace для приложения

urlpatterns = [
    path('', views.index, name='index'),  # Добавляем name
    path('create/', views.post_create, name='post_create'),
    path('posts/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('group/<slug:slug>/', views.group_posts, name='group_list'),
    path('groups/', views.groups_list, name='groups_list'),
    path('groups/search/', views.group_search, name='group_search'),
    path('profile/search/', views.profile_search, name='profile_search'),
]