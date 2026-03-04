from django.shortcuts import render

def index(request):
    """Главная страница Yatube"""
    template = 'posts/index.html'
    # Здесь в будущем будем передавать посты из базы данных
    context = {
        'title': 'Последние обновления на сайте',
        'text': 'Это главная страница проекта Yatube',
    }
    return render(request, template, context)

def group_posts(request, slug):
    """Страница с постами, отфильтрованными по группам"""
    template = 'posts/group_list.html'
    # Здесь в будущем будем передавать посты группы из базы данных
    context = {
        'slug': slug,
        'group_title': 'Лев Толстой – зеркало русской революции',
        'group_description': 'Группа тайных поклонников графа.',
        'text': 'Здесь будет информация о группах проекта Yatube',
    }
    return render(request, template, context)