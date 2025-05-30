"""
forms.py — Форма ввода данных

Определяет формы, которые используются на веб-страницах:
- DrugForm — форма добавления и редактирования препарата;
- DrugMovementForm — форма записи движения препарата (приход/расход).

Формы автоматически связываются с моделями и обеспечивают валидацию данных.
"""

from django import forms
from .models import Drug, DrugMovement

# Форма для добавления движения препарата (приход или расход)
class DrugMovementForm(forms.ModelForm):
    class Meta:
        model = DrugMovement  # Указываем, с какой моделью связана форма
        fields = ['movement_type', 'quantity', 'note']  # Какие поля будут в форме
        labels = {
            'movement_type': 'Тип движения',     # Подпись для поля (видимая пользователю)
            'quantity': 'Количество',
            'note': 'Примечание',
        }


# Форма для создания или редактирования препарата
class DrugForm(forms.ModelForm):
    class Meta:
        model = Drug  # Модель, с которой работает форма
        fields = [
            'name',            # Название препарата
            'form',            # Форма выпуска (таблетки, капли и т.д.)
            'manufacturer',    # Производитель
            'batch_number',    # Номер партии
            'expiration_date', # Срок годности
            'quantity'         # Количество (остаток на складе)
        ]
        labels = {
            'name': 'Название',
            'form': 'Форма выпуска',
            'manufacturer': 'Производитель',
            'batch_number': 'Номер партии',
            'expiration_date': 'Срок годности',
            'quantity': 'Количество',
        }
        widgets = {
            # Для удобства указываем, что поле "expiration_date" — это календарь
            'expiration_date': forms.DateInput(attrs={'type': 'date'}),
        }
