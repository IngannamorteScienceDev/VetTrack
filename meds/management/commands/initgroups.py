"""
initgroups.py — Команда Django для создания ролей и базовых прав доступа

Эта команда создаёт три группы пользователей:
- Администратор — получает все возможные права;
- Ветеринар — может просматривать препараты и добавлять назначения;
- Провизор — может управлять препаратами, но не видеть назначения.

Команда используется при первичной настройке системы.
Запуск: python manage.py initgroups
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from meds.models import Drug, DrugMovement

class Command(BaseCommand):
    help = 'Создаёт роли и назначает базовые права'

    def handle(self, *args, **kwargs):
        # Описание ролей и их прав
        groups = {
            'Администратор': {
                'permissions': 'all',  # Администратор получает все возможные права
            },
            'Ветеринар': {
                # Может добавлять назначения и просматривать препараты
                'permissions': ['add_drugmovement', 'view_drug', 'view_drugmovement'],
            },
            'Провизор': {
                # Может добавлять и редактировать препараты, но не видеть назначения
                'permissions': ['add_drug', 'change_drug', 'view_drug'],
            }
        }

        # Создаём группы и назначаем права
        for group_name, options in groups.items():
            group, created = Group.objects.get_or_create(name=group_name)

            if options['permissions'] == 'all':
                perms = Permission.objects.all()  # Все доступные права
            else:
                perms = Permission.objects.filter(codename__in=options['permissions'])

            group.permissions.set(perms)  # Назначаем права группе
            group.save()

            self.stdout.write(self.style.SUCCESS(f'Группа \"{group_name}\" обновлена'))
