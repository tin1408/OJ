import os
import django
from django.contrib.auth import get_user_model
from judge.models import Judge

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
    judge_name = "default_judge"
    judge_key = "default_judge_key"
    
    judge, created = Judge.objects.get_or_create(
        name=judge_name,
        defaults={
            'auth_key': judge_key,
            'is_blocked': False,
            'description': 'Default Judge'
        }
    )
    
    if created:
        print(f"Judge '{judge_name}' created.")
    else:
        if judge.auth_key != judge_key:
            judge.auth_key = judge_key
            judge.save()
            print(f"Judge '{judge_name}' key updated.")
        else:
            print(f"Judge '{judge_name}' already exists and is up to date.")

if __name__ == '__main__':
    create_admin()
    create_judge()
