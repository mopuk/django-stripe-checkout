import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        User = get_user_model()

        username = os.environ["DJANGO_ADMIN_USERNAME"]
        email = os.environ["DJANGO_ADMIN_EMAIL"]
        password = os.environ["DJANGO_ADMIN_PASSWORD"]

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
            )
