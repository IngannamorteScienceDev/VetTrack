from django.contrib import admin
from .models import Drug, DrugMovement


# Регистрируем модель Drug (Препарат) в административной панели Django
@admin.register(Drug)
class DrugAdmin(admin.ModelAdmin):
    # Какие поля отображать в таблице списка препаратов
    list_display = ("name", "form", "manufacturer", "expiration_date", "quantity")

    # Какие поля можно использовать для поиска (поиск сверху)
    search_fields = ("name", "form", "manufacturer")

    # Возможность фильтрации по этим полям (сбоку)
    list_filter = ("form", "expiration_date")


# Регистрируем модель DrugMovement (Движение препарата)
@admin.register(DrugMovement)
class DrugMovementAdmin(admin.ModelAdmin):
    # Отображаемые поля в списке движений
    list_display = ("drug", "movement_type", "quantity", "date")

    # Фильтры сбоку (например, фильтр по типу движения или дате)
    list_filter = ("movement_type", "date")

    # Поиск по названию препарата (через связанное поле)
    search_fields = ("drug__name",)
