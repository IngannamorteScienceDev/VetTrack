from django.db import models
from django.conf import settings
from datetime import date

class Drug(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    form = models.CharField(max_length=100, verbose_name="Форма выпуска")
    manufacturer = models.CharField(max_length=255, verbose_name="Производитель", blank=True)
    batch_number = models.CharField(max_length=100, verbose_name="Номер партии", blank=True)
    expiration_date = models.DateField(verbose_name="Срок годности")
    quantity = models.PositiveIntegerField(verbose_name="Количество (в штуках)")

    def __str__(self):
        return f"{self.name} ({self.form})"

    @property
    def is_expired(self):
        return date.today() > self.expiration_date

    @property
    def is_expiring_soon(self):
        return 0 <= (self.expiration_date - date.today()).days <= 7

class DrugMovement(models.Model):
    MOVEMENT_TYPE_CHOICES = [
        ('in', 'Приход'),
        ('out', 'Расход'),
    ]

    drug = models.ForeignKey(Drug, on_delete=models.CASCADE, verbose_name="Препарат")
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_TYPE_CHOICES, verbose_name="Тип движения")
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата")
    note = models.TextField(blank=True, verbose_name="Примечание")

    # 👇 Добавляем, кто создал запись
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Кем добавлено"
    )

    def __str__(self):
        return f"{self.get_movement_type_display()} {self.quantity} {self.drug.name}"
