#!/usr/bin/env python
"""
manage.py — Запуск административных команд Django

Это служебный файл, с которого начинается работа проекта.
Он используется для выполнения команд: запуск сервера, миграции, создание суперпользователя и т.д.

Примеры использования в терминале:
  python manage.py runserver          — запустить сервер
  python manage.py makemigrations     — создать миграции
  python manage.py migrate            — применить миграции
  python manage.py createsuperuser    — создать администратора
"""

import os
import sys

def main():
    """Основная точка входа для выполнения команд"""
    # Указываем Django, где находятся настройки проекта
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        # Импортируем функцию для запуска командной строки Django
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Если Django не установлен — выводим понятную ошибку
        raise ImportError(
            "Невозможно импортировать Django. Убедитесь, что он установлен "
            "и доступен в переменной окружения PYTHONPATH. "
            "Также проверьте, активировано ли виртуальное окружение."
        ) from exc

    # Запускаем команду, переданную через консоль
    execute_from_command_line(sys.argv)

# Если скрипт был запущен напрямую (а не импортирован), выполняем main()
if __name__ == '__main__':
    main()
