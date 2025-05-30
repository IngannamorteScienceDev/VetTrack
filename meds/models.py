from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import date

# Модель Препарата (основная сущность — что есть на складе)
class Drug(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")  # Название препарата
    form = models.CharField(max_length=100, verbose_name="Форма выпуска")  # Например: таблетки, ампулы
    manufacturer = models.CharField(max_length=255, verbose_name="Производитель", blank=True)  # Производитель (необяз.)
    batch_number = models.CharField(max_length=100, verbose_name="Номер партии", blank=True)  # Партия (необяз.)
    expiration_date = models.DateField(verbose_name="Срок годности")  # Когда заканчивается срок годности
    quantity = models.PositiveIntegerField(verbose_name="Количество (в штуках)")  # Остаток на складе
    is_archived = models.BooleanField(default=False, verbose_name="Архивирован")  # Отметка, что препарат убран в архив

    def __str__(self):
        # Как препарат будет отображаться в админке и списках
        return f"{self.name} ({self.form})"

    @property
    def is_expired(self):
        # Проверка: срок годности уже истёк?
        return date.today() > self.expiration_date

    @property
    def is_expiring_soon(self):
        # Проверка: истекает в течение 7 дней?
        return 0 <= (self.expiration_date - date.today()).days <= 7


# Модель Движения Препаратов (приход или расход)
class DrugMovement(models.Model):
    # Варианты движения: приход или расход
    MOVEMENT_TYPE_CHOICES = [
        ('in', 'Приход'),   # поступление на склад
        ('out', 'Расход'),  # списание или использование
    ]

    drug = models.ForeignKey(Drug, on_delete=models.CASCADE, verbose_name="Препарат")
    # Препарат, к которому относится это движение

    movement_type = models.CharField(
        max_length=3,
        choices=MOVEMENT_TYPE_CHOICES,
        verbose_name="Тип движения"
    )
    # Тип движения: in — приход, out — расход

    quantity = models.PositiveIntegerField(verbose_name="Количество")  # Сколько единиц пришло или ушло
    date = models.DateTimeField(default=timezone.now, verbose_name="Дата")  # Когда произошло движение
    note = models.TextField(blank=True, verbose_name="Примечание")  # Комментарий к записи (необязательный)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,        # стандартная модель пользователя Django
        on_delete=models.SET_NULL,       # если пользователь удалён — просто оставить пусто
        null=True,
        verbose_name="Кем добавлено"     # кто добавил движение
    )

    def __str__(self):
        # Как будет отображаться запись в админке: «Приход 10 Амоксициллин»
        return f"{self.get_movement_type_display()} {self.quantity} {self.drug.name}"
