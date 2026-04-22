# КиноМир — сообщество кинокритиков

Платформа для публикации рецензий на фильмы. Пользователи могут делиться мнениями, оценивать фильмы и объединять рецензии по жанрам.

## Быстрый старт

### Требования
- Python 3.9+
- Git

### Установка и запуск (автоматический)

```bash
# 1. Клонировать репозиторий
git clone <url-репозитория>
cd kinomir_project/kinomir

# 2. Запустить скрипт развёртывания
# Windows (Git Bash):
./run_windows.sh
# Linux/Mac:
./run_linux.sh
```

Скрипт сам создаст окружение, установит зависимости, выполнит миграции, загрузит тестовые данные и запустит сервер.

### Установка и запуск (ручной)

```bash
# 1. Клонировать репозиторий
git clone <url-репозитория>
cd kinomir_project/kinomir

# 2. Создать и активировать виртуальное окружение
python -m venv venv
source venv/Scripts/activate  # Windows (Git Bash)
source venv/bin/activate      # Linux/Mac

# 3. Установить зависимости
pip install -r requirements.txt
```

После запуска сайт доступен по адресу: http://127.0.0.1:8000/

## Основные команды

| Команда | Описание |
|---------|----------|
| `python manage.py runserver` | Запуск сервера |
| `python manage.py makemigrations` | Создание миграций |
| `python manage.py migrate` | Применение миграций |
| `python manage.py createsuperuser` | Создание админа |
| `python manage.py loaddata fixtures/kinomir_data.json` | Загрузка тестовых данных |
| `python save_fixture.py` | Сохранение новых данных в фикстуру (без ошибок кодировки) |

## Запуск тестов

```bash
python manage.py test                    # Все тесты
python manage.py test reviews            # Тесты приложения reviews
python manage.py test -v 2               # Подробный вывод
```

## Структура проекта

```
kinomir_project/
├── kinomir/
│   ├── reviews/          # Рецензии и жанры
│   ├── users/            # Регистрация/авторизация
│   ├── core/             # Общие компоненты
│   ├── about/            # Статические страницы
│   ├── static/           # CSS, изображения
│   ├── templates/        # HTML шаблоны
│   ├── fixtures/         # Дамп тестовых данных
│   │   └── kinomir_data.json
│   └── kinomir/          # Настройки проекта
├── manage.py
├── save_fixture.py       # Скрипт сохранения данных в фикстуру
├── run_windows.sh        # Скрипт запуска для Windows
├── run_linux.sh          # Скрипт запуска для Linux/Mac
└── requirements.txt      # Зависимости  
```

## Лицензия

Проект распространяется под лицензией BSD 3-Clause. Подробнее в файле [LICENSE](LICENSE).