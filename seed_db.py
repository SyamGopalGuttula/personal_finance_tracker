import os
import django
import random
from datetime import datetime, timedelta

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "finance_tracker.settings")
django.setup()

from core.models import Expense

# Clear existing expenses
Expense.objects.all().delete()

# Define categories and sample data
categories = ['Food', 'Transportation', 'Entertainment', 'Utilities', 'Other']
sample_titles = [
    'Groceries', 'Bus Ticket', 'Netflix Subscription', 
    'Electric Bill', 'Lunch', 'Movie Ticket', 'Gym Membership'
]
sample_descriptions = [
    'Monthly expense', 'One-time purchase', 
    'Online subscription', 'Paid in cash', 'Credit card payment'
]

# Generate random expenses
for _ in range(50):  # Adjust the number of test expenses here
    title = random.choice(sample_titles)
    amount = round(random.uniform(5, 100), 2)
    date = datetime.now() - timedelta(days=random.randint(0, 90))
    category = random.choice(categories)
    description = random.choice(sample_descriptions)

    Expense.objects.create(
        title=title,
        amount=amount,
        date=date,
        category=category,
        description=description
    )

print("✅ Database populated with test expenses.")