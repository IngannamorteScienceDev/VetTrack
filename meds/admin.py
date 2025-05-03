from django.contrib import admin
from .models import Drug, DrugMovement

@admin.register(Drug)
class DrugAdmin(admin.ModelAdmin):
    list_display = ("name", "form", "manufacturer", "expiration_date", "quantity")
    search_fields = ("name", "form", "manufacturer")
    list_filter = ("form", "expiration_date")

@admin.register(DrugMovement)
class DrugMovementAdmin(admin.ModelAdmin):
    list_display = ("drug", "movement_type", "quantity", "date")
    list_filter = ("movement_type", "date")
    search_fields = ("drug__name",)
