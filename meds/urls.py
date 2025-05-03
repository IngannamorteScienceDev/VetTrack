from django.urls import path
from . import views

urlpatterns = [
    path('drugs/', views.drug_list, name='drug_list'),
    path('drugs/<int:drug_id>/movement/', views.create_movement, name='create_movement'),
    path('drugs/create/', views.create_drug, name='create_drug'),
]
