"""
Management command to ensure the default admin user exists.
Run: python manage.py ensure_admin
"""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()
ADMIN_USERNAME = "lora"
ADMIN_PASSWORD = "lora@25"
ADMIN_EMAIL = "admin@lorarealestate.com"


class Command(BaseCommand):
    help = "Create the default admin user (lora/lora@25) if it does not exist."

    def handle(self, *args, **options):
        if User.objects.filter(username=ADMIN_USERNAME).exists():
            self.stdout.write(
                self.style.SUCCESS(f"Admin user '{ADMIN_USERNAME}' already exists.")
            )
            return

        User.objects.create_superuser(
            username=ADMIN_USERNAME,
            email=ADMIN_EMAIL,
            password=ADMIN_PASSWORD,
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"Admin user '{ADMIN_USERNAME}' created successfully. "
                f"Login at /admin/ with username={ADMIN_USERNAME}, password={ADMIN_PASSWORD}"
            )
        )
