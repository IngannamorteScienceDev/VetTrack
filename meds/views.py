from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.contrib import messages
from .models import Drug, DrugMovement
from .forms import DrugMovementForm


def is_veterinarian(user):
    return user.groups.filter(name="Ветеринар").exists() or user.is_superuser


@login_required
def drug_list(request):
    drugs = Drug.objects.all().order_by('expiration_date')
    today = timezone.now().date()

    # Генерируем список с пометками
    annotated_drugs = []
    for drug in drugs:
        if drug.expiration_date < today:
            status = 'expired'
        elif 0 <= (drug.expiration_date - today).days <= 7:
            status = 'soon'
        else:
            status = 'ok'

        annotated_drugs.append({
            'object': drug,
            'status': status,
        })

    return render(request, 'meds/drug_list.html', {'annotated_drugs': annotated_drugs})


@login_required
@user_passes_test(is_veterinarian)
def create_movement(request, drug_id):
    drug = get_object_or_404(Drug, id=drug_id)

    if request.method == 'POST':
        form = DrugMovementForm(request.POST)
        if form.is_valid():
            movement = form.save(commit=False)
            movement.drug = drug
            movement.created_by = request.user
            movement.save()

            # Автоматическое обновление количества в модели Drug
            if movement.movement_type == 'in':
                drug.quantity += movement.quantity
            elif movement.movement_type == 'out':
                if drug.quantity < movement.quantity:
                    messages.error(request, "Нельзя списать больше, чем есть.")
                    return redirect('drug_list')
                drug.quantity -= movement.quantity
            drug.save()

            messages.success(request, "Движение успешно добавлено.")
            return redirect('drug_list')
    else:
        form = DrugMovementForm()

    return render(request, 'meds/create_movement.html', {'form': form, 'drug': drug})
