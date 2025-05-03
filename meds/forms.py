from django import forms
from .models import DrugMovement

class DrugMovementForm(forms.ModelForm):
    class Meta:
        model = DrugMovement
        fields = ['movement_type', 'quantity', 'note']
        labels = {
            'movement_type': 'Тип движения',
            'quantity': 'Количество',
            'note': 'Примечание',
        }
