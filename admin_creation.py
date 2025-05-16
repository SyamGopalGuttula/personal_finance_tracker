from django.contrib.auth.models import User

# Check if the Admin user exists
if not User.objects.filter(username='admin').exists():
    User.objects.create_user(username='admin', password='adminpassword', email='admin@example.com')
    print("Admin user created.")
else:
    print("Admin user already exists.")
