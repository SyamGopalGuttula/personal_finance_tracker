from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense  # Importing the Expense model
from .forms import ExpenseForm  # Importing the ExpenseForm
from django.db.models import Q, Sum  
from django.http import HttpResponse  # Add this line
import csv
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.db.models import Q

def register_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already in use.")
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                messages.success(request, "Account created successfully. You can now log in.")
                return redirect('login')
        else:
            messages.error(request, "Passwords do not match.")
    
    return render(request, 'core/register.html')

def download_analytics_csv(request):
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

    # Calculate analytics
    total_expenses = expenses.aggregate(total=Sum('amount'))['total'] or 0
    expense_breakdown = expenses.values('category').annotate(total=Sum('amount')).order_by('-total')
    top_expenses = expenses.order_by('-amount')[:5]

    # Create CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=expense_analytics.csv'
    writer = csv.writer(response)

    # Write headers
    writer.writerow(['Expense Analytics Report'])
    writer.writerow(['Total Expenses', f'${total_expenses}'])

    writer.writerow([])
    writer.writerow(['Expense Breakdown by Category'])
    writer.writerow(['Category', 'Total Amount'])
    for item in expense_breakdown:
        writer.writerow([item['category'], f"${item['total']}"])

    writer.writerow([])
    writer.writerow(['Top 5 Expenses'])
    writer.writerow(['Title', 'Amount', 'Category'])
    for expense in top_expenses:
        writer.writerow([expense.title, f"${expense.amount}", expense.category])

    return response

@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user)  # Only show logged-in user's expenses
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

    # Summarization and Analytics
    total_expenses = expenses.aggregate(total=Sum('amount'))['total'] or 0
    expense_breakdown = expenses.values('category').annotate(total=Sum('amount')).order_by('-total')
    top_expenses = expenses.order_by('-amount')[:5]

    return render(request, 'core/expense_list.html', {
        'expenses': expenses,
        'form': form,
        'categories': categories,
        'selected_category': category,
        'query': query,
        'start_date': start_date,
        'end_date': end_date,
        'total_expenses': total_expenses,
        'expense_breakdown': expense_breakdown,
        'top_expenses': top_expenses
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