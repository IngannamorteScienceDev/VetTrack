from django.urls import path
from . import views

urlpatterns = [
    path('drugs/', views.drug_list, name='drug_list'),
    path('drugs/<int:drug_id>/movement/', views.create_movement, name='create_movement'),
]
