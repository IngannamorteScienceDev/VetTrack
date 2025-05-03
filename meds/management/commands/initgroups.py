from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from meds.models import Drug, DrugMovement

class Command(BaseCommand):
    help = 'Создаёт роли и назначает базовые права'

    def handle(self, *args, **kwargs):
        groups = {
            'Администратор': {
                'permissions': 'all',
            },
            'Ветеринар': {
                'permissions': ['add_drugmovement', 'view_drug', 'view_drugmovement'],
            },
            'Провизор': {
                'permissions': ['add_drug', 'change_drug', 'view_drug'],
            }
        }

        for group_name, options in groups.items():
            group, created = Group.objects.get_or_create(name=group_name)
            if options['permissions'] == 'all':
                perms = Permission.objects.all()
            else:
                perms = Permission.objects.filter(codename__in=options['permissions'])

            group.permissions.set(perms)
            group.save()
            self.stdout.write(self.style.SUCCESS(f'Группа "{group_name}" обновлена'))
