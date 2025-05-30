# Импорт стандартных библиотек Python
import os           # позволяет работать с операционной системой (переменные окружения и т.п.)
import django       # импортируем Django — основной фреймворк проекта
import random       # библиотека для генерации случайных чисел и элементов
from datetime import timedelta, date  # для работы с датами
from django.utils import timezone     # специальный модуль Django для работы с временем

# Настраиваем окружение Django, указывая, где находятся настройки проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()  # инициализируем Django — без этого невозможно работать с базой данных

# Импортируем модели из приложения meds
from meds.models import Drug, DrugMovement
from django.contrib.auth.models import User  # импорт стандартной модели пользователя

# Получаем первого администратора (чтобы указать его как автора операций с препаратами)
admin = User.objects.filter(is_superuser=True).first()

# Получаем текущую дату (на сегодня)
today = date.today()

# Базовые части названий препаратов — будем из них случайно составлять имена
names_base = [
    "Амокси", "Цефтри", "Кето", "Преди", "Тило", "Ивер", "Гентами",
    "Ципро", "Фура", "Энро", "Декса", "Мильбе", "Синул", "Байтрил",
    "Ронко", "Флоро", "Седук", "Флура", "Карб", "Левами", "Хлора", "Папав"
]

# Возможные формы выпуска препаратов
forms = ["Таблетки", "Ампулы", "Раствор", "Порошок", "Капли", "Инъекция"]

# Возможные производители препаратов
manufacturers = ["ВетФарм", "БиоСинтез", "ФармВет", "Зоомедика", "Агровет", "Микрофарм"]

# Указываем, сколько препаратов хотим добавить в базу данных
total_drugs = 120

# Основной цикл — создаём 120 случайных препаратов
for i in range(total_drugs):
    # Генерируем уникальное название, например: "Ципро-47"
    name = f"{random.choice(names_base)}-{random.randint(10,99)}"

    # Создаём запись в таблице Drug (лекарства)
    drug = Drug.objects.create(
        name=name,
        form=random.choice(forms),  # случайная форма выпуска
        manufacturer=random.choice(manufacturers),  # случайный производитель
        batch_number=f"B{1000+i}",  # уникальный номер партии, например: B1000, B1001, ...
        expiration_date=today + timedelta(days=random.randint(-30, 365)),  # срок годности (может быть уже истёк)
        quantity=random.randint(5, 200)  # общее количество препарата на складе
    )

    # Для каждого препарата создаём 3–5 случайных движений (приход или расход)
    for _ in range(random.randint(3, 5)):
        movement_type = random.choice(['in', 'out'])  # приход или расход
        quantity = random.randint(1, 30)  # сколько единиц поступило/ушло
        note = f"{'Поступление' if movement_type == 'in' else 'Назначение'} #{random.randint(1000,9999)}"  # примечание
        date_offset = random.randint(-60, 0)  # случайная дата в пределах последних 60 дней
        date_value = timezone.now() + timedelta(days=date_offset)  # вычисляем дату события

        # Создаём запись о движении препарата в таблице DrugMovement
        DrugMovement.objects.create(
            drug=drug,
            movement_type=movement_type,
            quantity=quantity,
            date=date_value,
            note=note,
            created_by=admin  # указываем, что движение добавил администратор
        )

# Сообщение в консоль о завершении генерации данных
print(f"✅ Добавлено {total_drugs} препаратов и движение к каждому.")
