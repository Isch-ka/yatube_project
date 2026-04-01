from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import PostForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth import get_user_model
from .models import Post, Group

User = get_user_model()

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
@login_required
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
        # Перенаправляем на страницу профайла пользователя
        return redirect('posts:profile', username=request.user.username)
    
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
        return redirect('posts:profile', username=request.user.username)
    
    form = PostForm(request.POST or None, instance=post)
    
    if request.method == 'POST' and form.is_valid():
        form.save()
        # После редактирования тоже перенаправляем на страницу профайла
        return redirect('posts:profile', username=request.user.username)
    
    context = {
        'form': form,
        'is_edit': True,
        'post_id': post_id,
    }
    return render(request, 'posts/post_form.html', context)


def profile(request, username):
    """Профайл пользователя"""
    author = get_object_or_404(User, username=username)
    post_list = author.posts.select_related('group').order_by('-pub_date')
    
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'author': author,
        'page_obj': page_obj,
        'total_posts': post_list.count(),
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    """Страница отдельного поста"""
    post = get_object_or_404(Post, id=post_id)
    total_posts = post.author.posts.count()
    
    context = {
        'post': post,
        'total_posts': total_posts,
    }
    return render(request, 'posts/post_detail.html', context)


def profile_search(request):
    """Поиск пользователей по имени или username"""
    query = request.GET.get('q', '')
    users = User.objects.all()
    
    if query:
        users = users.filter(
            Q(username__icontains=query) | 
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query)
        ).order_by('username')
    
    paginator = Paginator(users, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'total_users': users.count(),
    }
    return render(request, 'posts/profile_search.html', context)