# your_app_name/management/commands/create_initial_superuser.py
import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = "Creates a manager non-interactively if none exist, using environment variables."

    def handle(self, *args, **options):
        # Check if any superuser already exists
        if User.objects.filter(role=User.Role.MANAGER).exists():
            self.stdout.write(self.style.SUCCESS("A manager already exists. Skipping creation."))
            return

        # Read credentials from environment variables
        username = os.environ.get("INITIAL_MANAGER_USERNAME")
        email = os.environ.get("INITIAL_MANAGER_EMAIL")
        password = os.environ.get("INITIAL_MANAGER_PASSWORD")

        # Validate that all variables are set
        if not all([username, email, password]):
            self.stderr.write(
                self.style.ERROR(
                    "Missing environment variables: INITIAL_MANAGER_USERNAME, "
                    "INITIAL_MANAGER_EMAIL, INITIAL_MANAGER_PASSWORD"
                )
            )
            # Optionally raise an error to stop startup if desired
            # raise ImproperlyConfigured("Missing superuser credentials in environment variables")
            return  # Or just exit gracefully

        # Create the superuser
        self.stdout.write(f"Creating manager '{username}'...")
        try:
            User.objects.create_user(
                username=username, email=email, password=password, role=User.Role.MANAGER, is_staff=True
            )
            self.stdout.write(self.style.SUCCESS(f"Manager '{username}' created successfully."))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error creating manager: {e}"))
