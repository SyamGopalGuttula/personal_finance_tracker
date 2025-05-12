from django.urls import path
from . import views  # Importing views from this app

urlpatterns = [
    path('', views.expense_list, name='expense_list'),  # This URL will show the list of expenses
]

