import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        User = get_user_model()

        users = [
            {
                "username": os.environ["DJANGO_ADMIN_USERNAME"],
                "email": os.environ["DJANGO_ADMIN_EMAIL"],
                "password": os.environ["DJANGO_ADMIN_PASSWORD"],
            },
            {
                "username": os.environ["DJANGO_REVIEWER_USERNAME"],
                "email": os.environ["DJANGO_REVIEWER_EMAIL"],
                "password": os.environ["DJANGO_REVIEWER_PASSWORD"],
            },
        ]

        for user_data in users:
            if not User.objects.filter(username=user_data["username"]).exists():
                User.objects.create_superuser(**user_data)
                self.stdout.write(f"Created superuser: {user_data['username']}")
