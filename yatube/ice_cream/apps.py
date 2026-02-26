# anfisa/ice_cream/apps.py
from django.apps import AppConfig


class IceCreamConfig(AppConfig):
    name = 'ice_cream'
    # Тут можно указать, например, поле verbose_name
    # под этим именем приложение будет видно в админке.
    # verbose_name = 'Управление сортами мороженого'