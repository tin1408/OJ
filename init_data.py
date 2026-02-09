import os
import django
from django.contrib.auth import get_user_model
from judge.models import Judge

# When run via 'manage.py shell < init_data.py', django is already setup.
# But keeping these for safety if run directly.
if not os.environ.get('DJANGO_SETTINGS_MODULE'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dmoj.settings')
    django.setup()

User = get_user_model()

def create_admin():
    if not User.objects.filter(username='admin').exists():
        print("Creating admin user...")
        User.objects.create_superuser('admin', 'admin@example.com', 'admin')
        print("Admin user created.")
    else:
        print("Admin user already exists.")

def create_judge():
    # Use environment variable if available, otherwise fallback to default
    judge_name = "default_judge"
    judge_key = os.environ.get('JUDGE_KEY', 'default_judge_key')
    
    judge, created = Judge.objects.get_or_create(
        name=judge_name,
        defaults={
            'auth_key': judge_key,
            'is_blocked': False,
            'description': 'Default Judge'
        }
    )
    
    if created:
        print(f"Judge '{judge_name}' created with key: {judge_key}")
    else:
        if judge.auth_key != judge_key:
            judge.auth_key = judge_key
            judge.save()
            print(f"Judge '{judge_name}' key updated to: {judge_key}")
        else:
            print(f"Judge '{judge_name}' already exists and key is correct.")

# Run the functions
create_admin()
create_judge()
