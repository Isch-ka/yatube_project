from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse


def group_required(group_slug):
    """Декоратор для проверки, входит ли пользователь в группу"""
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                # Проверяем, есть ли у пользователя доступ к группе
                return func(request, *args, **kwargs)
            return redirect(reverse('users:login'))
        return wrapper
    return decorator


def cache_result(func):
    """Простой декоратор для кэширования результатов функции"""
    cache = {}
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    
    return wrapper


@cache_result
def expensive_operation(n):
    """Пример функции с кэшированием"""
    import time
    time.sleep(2)
    return n * 2