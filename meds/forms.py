from django import forms
from .models import Drug, DrugMovement

class DrugMovementForm(forms.ModelForm):
    class Meta:
        model = DrugMovement
        fields = ['movement_type', 'quantity', 'note']
        labels = {
            'movement_type': 'Тип движения',
            'quantity': 'Количество',
            'note': 'Примечание',
        }

class DrugForm(forms.ModelForm):
    class Meta:
        model = Drug
        fields = ['name', 'form', 'manufacturer', 'batch_number', 'expiration_date', 'quantity']
        labels = {
            'name': 'Название',
            'form': 'Форма выпуска',
            'manufacturer': 'Производитель',
            'batch_number': 'Номер партии',
            'expiration_date': 'Срок годности',
            'quantity': 'Количество',
        }
        widgets = {
            'expiration_date': forms.DateInput(attrs={'type': 'date'}),
        }
