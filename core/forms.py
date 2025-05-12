from django import forms
from .models import Expense
from datetime import date

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['title', 'amount', 'date', 'category', 'description']

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError("Amount must be greater than zero.")
        return amount

    def clean_date(self):
        expense_date = self.cleaned_data.get('date')
        if expense_date > date.today():
            raise forms.ValidationError("Date cannot be in the future.")
        return expense_date
