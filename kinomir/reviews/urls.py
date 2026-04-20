from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.review_create, name='review_create'),
    path('reviews/<int:review_id>/', views.review_detail, name='review_detail'),
    path('reviews/<int:review_id>/edit/', views.review_edit, name='review_edit'),
    path('reviews/<int:review_id>/moderate/', views.review_moderate, name='review_moderate'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('profile/search/', views.profile_search, name='profile_search'),
    path('genre/<slug:slug>/', views.genre_reviews, name='genre_list'),
    path('genres/', views.genres_list, name='genres_list'),
]