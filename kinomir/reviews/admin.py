from django.contrib import admin
from .models import Review, Genre


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('movie_title', 'director', 'release_year', 'rating', 'author', 'is_approved', 'pub_date')
    list_filter = ('is_approved', 'genre', 'rating', 'release_year')
    search_fields = ('movie_title', 'director', 'author__username', 'text')
    list_editable = ('is_approved',)
    date_hierarchy = 'pub_date'