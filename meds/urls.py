from django.urls import path
from . import views

urlpatterns = [
    path('drugs/', views.drug_list, name='drug_list'),
    path('drugs/<int:drug_id>/movement/', views.create_movement, name='create_movement'),
    path('drugs/create/', views.create_drug, name='create_drug'),
    path('drugs/<int:drug_id>/history/', views.drug_history, name='drug_history'),
    path('drugs/<int:drug_id>/export_excel/', views.export_drug_history_excel, name='export_drug_history_excel'),
    path('drug/<int:drug_id>/edit/', views.edit_drug, name='edit_drug'),
    path('drug/<int:drug_id>/toggle-archive/', views.toggle_archive_drug, name='toggle_archive_drug'),
    path('report/', views.movement_report, name='movement_report'),
]
