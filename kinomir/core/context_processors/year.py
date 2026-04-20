import datetime


def year(request):
    """Добавляет в контекст переменную с текущим годом"""
    now = datetime.datetime.now()
    return {
        'year': now.year
    }