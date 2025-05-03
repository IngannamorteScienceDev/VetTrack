from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.contrib import messages
from .models import Drug, DrugMovement
from .forms import DrugMovementForm, DrugForm  # ← обновлено

import openpyxl
from django.http import HttpResponse

def is_veterinarian(user):
    return user.groups.filter(name="Ветеринар").exists() or user.is_superuser


@login_required
def drug_list(request):
    drugs = Drug.objects.all().order_by('expiration_date')
    today = timezone.now().date()
    status_filter = request.GET.get('status')

    annotated_drugs = []
    for drug in drugs:
        if drug.expiration_date < today:
            status = 'expired'
        elif 0 <= (drug.expiration_date - today).days <= 7:
            status = 'soon'
        else:
            status = 'ok'

        if status_filter and status != status_filter:
            continue

        annotated_drugs.append({
            'object': drug,
            'status': status,
        })

    return render(request, 'meds/drug_list.html', {
        'annotated_drugs': annotated_drugs,
        'active_filter': status_filter
    })


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


@login_required
def create_drug(request):
    if request.method == 'POST':
        form = DrugForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Препарат успешно добавлен.")
            return redirect('drug_list')
    else:
        form = DrugForm()

    return render(request, 'meds/create_drug.html', {'form': form})

@login_required
def drug_history(request, drug_id):
    drug = get_object_or_404(Drug, id=drug_id)
    movements = DrugMovement.objects.filter(drug=drug).order_by('-date')

    return render(request, 'meds/drug_history.html', {
        'drug': drug,
        'movements': movements,
    })

@login_required
def export_drug_history_excel(request, drug_id):
    drug = get_object_or_404(Drug, id=drug_id)
    movements = DrugMovement.objects.filter(drug=drug).order_by('-date')

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "История движения"

    # Заголовки
    ws.append(["Дата", "Тип", "Количество", "Примечание"])

    # Данные
    for move in movements:
        ws.append([
            move.date.strftime("%d.%m.%Y %H:%M"),
            "Приход" if move.movement_type == 'in' else "Расход",
            move.quantity,
            move.note or ""
        ])

    # Отправка файла
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    from django.utils.text import slugify
    filename = f"history_{slugify(drug.name)}.xlsx"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    wb.save(response)
    return response