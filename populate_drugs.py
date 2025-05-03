import os
import django
import random
from datetime import timedelta, date
from django.utils import timezone

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from meds.models import Drug, DrugMovement
from django.contrib.auth.models import User

admin = User.objects.filter(is_superuser=True).first()
today = date.today()

names_base = [
    "Амокси", "Цефтри", "Кето", "Преди", "Тило", "Ивер", "Гентами",
    "Ципро", "Фура", "Энро", "Декса", "Мильбе", "Синул", "Байтрил",
    "Ронко", "Флоро", "Седук", "Флура", "Карб", "Левами", "Хлора", "Папав"
]
forms = ["Таблетки", "Ампулы", "Раствор", "Порошок", "Капли", "Инъекция"]
manufacturers = ["ВетФарм", "БиоСинтез", "ФармВет", "Зоомедика", "Агровет", "Микрофарм"]

total_drugs = 120

for i in range(total_drugs):
    name = f"{random.choice(names_base)}-{random.randint(10,99)}"
    drug = Drug.objects.create(
        name=name,
        form=random.choice(forms),
        manufacturer=random.choice(manufacturers),
        batch_number=f"B{1000+i}",
        expiration_date=today + timedelta(days=random.randint(-30, 365)),
        quantity=random.randint(5, 200)
    )

    # Движения: 3–5 случайных
    for _ in range(random.randint(3, 5)):
        movement_type = random.choice(['in', 'out'])
        quantity = random.randint(1, 30)
        note = f"{'Поступление' if movement_type == 'in' else 'Назначение'} #{random.randint(1000,9999)}"
        date_offset = random.randint(-60, 0)  # за последние 60 дней
        date_value = timezone.now() + timedelta(days=date_offset)

        DrugMovement.objects.create(
            drug=drug,
            movement_type=movement_type,
            quantity=quantity,
            date=date_value,
            note=note,
            created_by=admin
        )

print(f"✅ Добавлено {total_drugs} препаратов и движение к каждому.")
