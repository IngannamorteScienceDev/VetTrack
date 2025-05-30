from django.urls import path
from . import views  # Импортируем функции (представления), которые будут привязаны к адресам

# Здесь мы определяем список всех URL-адресов (маршрутов), которые доступны в приложении
urlpatterns = [
    # Страница со списком всех препаратов
    path('drugs/', views.drug_list, name='drug_list'),

    # Добавление движения (приход или расход) для конкретного препарата
    path('drugs/<int:drug_id>/movement/', views.create_movement, name='create_movement'),

    # Создание нового препарата
    path('drugs/create/', views.create_drug, name='create_drug'),

    # История всех движений по конкретному препарату
    path('drugs/<int:drug_id>/history/', views.drug_history, name='drug_history'),

    # Выгрузка истории препарата в Excel
    path('drugs/<int:drug_id>/export_excel/', views.export_drug_history_excel, name='export_drug_history_excel'),

    # Редактирование информации о препарате
    path('drug/<int:drug_id>/edit/', views.edit_drug, name='edit_drug'),

    # Архивация или восстановление препарата
    path('drug/<int:drug_id>/toggle-archive/', views.toggle_archive_drug, name='toggle_archive_drug'),

    # Общий отчёт по движениям всех препаратов
    path('report/', views.movement_report, name='movement_report'),

    # Главная страница (можно использовать как панель или приветствие)
    path('', views.index, name='index'),

    # Экспорт общего отчёта по движениям в Excel
    path('report/export/', views.movement_report_export_excel, name='movement_report_export_excel'),
]
