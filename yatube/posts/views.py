from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import PostForm
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Post, Group


def index(request):
    """Главная страница Yatube с поиском по постам"""
    # Базовый запрос - все посты
    post_list = Post.objects.all().order_by('-pub_date')

    # Получаем поисковый запрос из GET-параметров
    query = request.GET.get('q', '')
    
    # Если есть поисковый запрос, фильтруем посты
    if query:
        post_list = post_list.filter(text__icontains=query)
    
    # Применяем select_related для оптимизации запросов
    post_list = post_list.select_related('author', 'group')
    
    # Пагинация
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'total_posts': Post.objects.count(),
        'query': query,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    """Страница с постами группы"""
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.order_by('-pub_date')

    # Оптимизация запросов
    post_list = post_list.select_related('author')
    
    # Пагинация
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'group': group,
        'page_obj': page_obj,
        'total_posts': post_list.count(),
    }
    return render(request, 'posts/group_list.html', context)

def groups_list(request):
    """Страница со списком всех групп"""
    groups = Group.objects.all().order_by('title')
    
    # Добавляем количество постов для каждой группы
    for group in groups:
        group.posts_count = group.posts.count()
    
    paginator = Paginator(groups, 12)  # 12 групп на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'total_groups': Group.objects.count(),
        'total_posts': Post.objects.count(),
    }
    return render(request, 'posts/groups_list.html', context)


def group_search(request):
    """Поиск групп по названию или описанию"""
    query = request.GET.get('q', '')
    groups = Group.objects.all()
    
    if query:
        groups = groups.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        ).order_by('title')
    
    # Добавляем количество постов для каждой группы
    for group in groups:
        group.posts_count = group.posts.count()
    
    paginator = Paginator(groups, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'total_groups': groups.count(),
        'query': query,
        'total_posts': Post.objects.count(),
    }
    return render(request, 'posts/groups_list.html', context)

# Декоратор для создания поста
def post_create(request):
    """Страница создания нового поста (доступна только авторизованным)"""
    form = PostForm(request.POST or None)
    
    if request.method == 'POST' and form.is_valid():
        # Создаём пост, но пока не сохраняем в БД
        post = form.save(commit=False)
        # Присваиваем автору текущего пользователя
        post.author = request.user
        # Сохраняем пост в БД
        post.save()
        # Перенаправляем на главную страницу
        return redirect('posts:index')
    
    context = {
        'form': form,
        'is_edit': False,  # Для различения создания и редактирования
    }
    return render(request, 'posts/post_form.html', context)


@login_required
def post_edit(request, post_id):
    """Страница редактирования поста (только для автора)"""
    post = get_object_or_404(Post, id=post_id)
    
    # Проверяем, что редактирует пост его автор
    if post.author != request.user:
        return redirect('posts:index')
    
    form = PostForm(request.POST or None, instance=post)
    
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('posts:index')
    
    context = {
        'form': form,
        'is_edit': True,
        'post_id': post_id,
    }
    return render(request, 'posts/post_form.html', context)