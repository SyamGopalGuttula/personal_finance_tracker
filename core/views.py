from django.shortcuts import render, redirect
from .models import Expense  # Importing the Expense model
from .forms import ExpenseForm  # Importing the ExpenseForm

def expense_list(request):
    expenses = Expense.objects.all()  # Fetching all expenses from the database

    # Handling the form submission
    if request.method == 'POST':
        # Here you would handle the form submission
        # For example, you could create a new expense or update an existing one
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = ExpenseForm()
    return render(request, 'core/expense_list.html', {'expenses': expenses, 'form': form})
