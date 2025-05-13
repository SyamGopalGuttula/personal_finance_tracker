from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense  # Importing the Expense model
from .forms import ExpenseForm  # Importing the ExpenseForm
from django.db.models import Q  

from django.db.models import Q

def expense_list(request):
    expenses = Expense.objects.all()
    query = request.GET.get('q') or ""
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    category = request.GET.get('category')

    if query and query.lower() != "none":
        expenses = expenses.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    if start_date:
        expenses = expenses.filter(date__gte=start_date)

    if end_date:
        expenses = expenses.filter(date__lte=end_date)

    if category and category != "All":
        expenses = expenses.filter(category__iexact=category.strip())


    form = ExpenseForm()
    categories = Expense.objects.values_list('category', flat=True).distinct()

    return render(request, 'core/expense_list.html', {
        'expenses': expenses,
        'form': form,
        'categories': categories,
        'selected_category': category,
        'query': query,
        'start_date': start_date,
        'end_date': end_date
    })



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