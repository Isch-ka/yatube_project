from django.shortcuts import render

def index(request):
    """Главная страница Yatube"""
    template = 'posts/index.html'
    return render(request, template)

def group_posts(request, slug):
    """Страница с постами, отфильтрованными по группам"""
    template = 'posts/group_list.html'
    context = {
        'slug': slug,
    }
    return render(request, template, context)