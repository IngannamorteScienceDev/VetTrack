from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.contrib import messages
from .models import Drug, DrugMovement
from .forms import DrugMovementForm, DrugForm
from django.core.paginator import Paginator
from django.utils.dateparse import parse_date
from django.db.models import Q
from django.http import HttpResponse
from django.utils.text import slugify
import openpyxl
from datetime import timedelta

def is_veterinarian(user):
    return user.groups.filter(name="Ветеринар").exists() or user.is_superuser


@login_required
def drug_list(request):
    show_archived = request.GET.get('archived') == '1'
    if show_archived:
        drugs = Drug.objects.filter(is_archived=True).order_by('expiration_date')
    else:
        drugs = Drug.objects.filter(is_archived=False).order_by('expiration_date')
    today = timezone.now().date()
    status_filter = request.GET.get('status')
    search_query = request.GET.get('search', '').strip()

    if search_query:
        drugs = drugs.filter(name__icontains=search_query)

    annotated = []
    for drug in drugs:
        if drug.expiration_date < today:
            status = 'expired'
        elif 0 <= (drug.expiration_date - today).days <= 7:
            status = 'soon'
        else:
            status = 'ok'

        if status_filter and status != status_filter:
            continue

        annotated.append({'object': drug, 'status': status})

    paginator = Paginator(annotated, 25)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'meds/drug_list.html', {
        'page_obj': page_obj,
        'active_filter': status_filter,
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
    movements = DrugMovement.objects.filter(drug=drug)

    # Получаем параметры фильтра
    start_date_str = request.GET.get("start_date")
    end_date_str = request.GET.get("end_date")
    quick = request.GET.get("quick")

    # Обработка быстрых фильтров
    today = timezone.now()
    if quick == "7":
        start_date = today - timedelta(days=7)
        end_date = today
    elif quick == "30":
        start_date = today - timedelta(days=30)
        end_date = today
    else:
        start_date = parse_date(start_date_str) if start_date_str else None
        end_date = parse_date(end_date_str) if end_date_str else None

    # Применение фильтра
    if start_date and end_date:
        movements = movements.filter(date__date__range=(start_date, end_date))
    elif start_date:
        movements = movements.filter(date__date__gte=start_date)
    elif end_date:
        movements = movements.filter(date__date__lte=end_date)

    movements = movements.order_by('-date')

    return render(request, 'meds/drug_history.html', {
        'drug': drug,
        'movements': movements,
        'start_date': start_date_str,
        'end_date': end_date_str,
        'quick': quick,
    })


@login_required
def export_drug_history_excel(request, drug_id):
    drug = get_object_or_404(Drug, id=drug_id)
    movements = DrugMovement.objects.filter(drug=drug).order_by('-date')

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "История движения"

    ws.append(["Дата", "Тип", "Количество", "Примечание"])

    for move in movements:
        ws.append([
            move.date.strftime("%d.%m.%Y %H:%M"),
            "Приход" if move.movement_type == 'in' else "Расход",
            move.quantity,
            move.note or ""
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    filename = f"history_{slugify(drug.name)}.xlsx"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    wb.save(response)
    return response

@login_required
@user_passes_test(is_veterinarian)
def edit_drug(request, drug_id):
    drug = get_object_or_404(Drug, id=drug_id)

    if request.method == 'POST':
        form = DrugForm(request.POST, instance=drug)
        if form.is_valid():
            form.save()
            messages.success(request, "Препарат обновлён.")
            return redirect('drug_list')
    else:
        form = DrugForm(instance=drug)

    return render(request, 'meds/edit_drug.html', {'form': form, 'drug': drug})

@login_required
@user_passes_test(is_veterinarian)
def toggle_archive_drug(request, drug_id):
    drug = get_object_or_404(Drug, id=drug_id)
    drug.is_archived = not drug.is_archived
    drug.save()
    if drug.is_archived:
        messages.info(request, f"Препарат «{drug.name}» архивирован.")
    else:
        messages.success(request, f"Препарат «{drug.name}» восстановлен.")
    return redirect('drug_list')

@login_required
def movement_report(request):
    movements = DrugMovement.objects.select_related("drug").order_by('-date')

    start_date_str = request.GET.get("start_date")
    end_date_str = request.GET.get("end_date")
    movement_type = request.GET.get("type")
    quick = request.GET.get("quick")

    # Быстрые фильтры
    today = timezone.now()
    if quick == "7":
        start_date = today - timedelta(days=7)
        end_date = today
    elif quick == "30":
        start_date = today - timedelta(days=30)
        end_date = today
    else:
        start_date = parse_date(start_date_str) if start_date_str else None
        end_date = parse_date(end_date_str) if end_date_str else None

    # Применяем фильтры
    if start_date and end_date:
        movements = movements.filter(date__date__range=(start_date, end_date))
    elif start_date:
        movements = movements.filter(date__date__gte=start_date)
    elif end_date:
        movements = movements.filter(date__date__lte=end_date)

    if movement_type in ["in", "out"]:
        movements = movements.filter(movement_type=movement_type)

    return render(request, 'meds/movement_report.html', {
        'movements': movements,
        'start_date': start_date_str,
        'end_date': end_date_str,
        'quick': quick,
        'active_type': movement_type
    })

def index(request):
    return render(request, 'meds/index.html')
