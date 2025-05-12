from django.shortcuts import render, redirect, get_object_or_404
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
def edit_expense(request, id):
    expense = get_object_or_404(Expense, id=id)

    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = ExpenseForm(instance=expense)

    return render(request, 'core/edit_expense.html', {'form': form, 'expense': expense})

def delete_expense(request, id):
    expense = get_object_or_404(Expense, id=id)
    if request.method == "POST":
        expense.delete()
        return redirect('/')
    return render(request, 'core/delete_expense.html', {'expense': expense})