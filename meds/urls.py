from django.urls import path
from . import views

urlpatterns = [
    path('drugs/', views.drug_list, name='drug_list'),
    path('drugs/<int:drug_id>/movement/', views.create_movement, name='create_movement'),
    path('drugs/create/', views.create_drug, name='create_drug'),
    path('drugs/<int:drug_id>/history/', views.drug_history, name='drug_history'),
    path('drugs/<int:drug_id>/export_excel/', views.export_drug_history_excel, name='export_drug_history_excel'),

]
