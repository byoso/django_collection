import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()

class Command(BaseCommand):
    """Auto create an admin user on start if it does not already exists"""

    def handle(self, *args, **options):

        if os.environ.get('CREATE_DJANGO_SUPERUSER', '0') == '1':
            username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
            password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
            email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_superuser(username, email, password)
                print(f'Superuser "{user.username}" created!')
            else:
                print('Superuser already exists!')
