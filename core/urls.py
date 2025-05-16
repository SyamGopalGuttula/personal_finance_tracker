from django.urls import path
from . import views  # Importing views from this app

urlpatterns = [
    path('', views.expense_list, name='expense_list'),
    path('register/', views.register_user, name='register'),
    path('edit/<int:id>/', views.edit_expense, name='edit_expense'),
    path('delete/<int:id>/', views.delete_expense, name='delete_expense'),
    path('download-analytics/', views.download_analytics_csv, name='download_analytics'),
]