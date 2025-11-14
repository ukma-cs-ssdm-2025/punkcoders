# your_app_name/management/commands/create_initial_superuser.py
import os

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

User = get_user_model()


class Command(BaseCommand):
    help = "Creates a manager non-interactively if none exist, using environment variables."

    def handle(self, *args, **options):
        # Check if any superuser already exists
        if User.objects.filter(role=User.Role.MANAGER).exists():
            self.stdout.write(self.style.SUCCESS("A manager already exists. Skipping creation."))
            return

        # Read credentials from environment variables
        email = os.environ.get("INITIAL_MANAGER_EMAIL")
        password = os.environ.get("INITIAL_MANAGER_PASSWORD")
        first_name = os.environ.get("INITIAL_MANAGER_FIRST_NAME")
        last_name = os.environ.get("INITIAL_MANAGER_LAST_NAME")

        # Validate that all variables are set
        if not all([email, password, first_name, last_name]):
            self.stderr.write(
                self.style.ERROR(
                    "Missing environment variables: "
                    "INITIAL_MANAGER_EMAIL, INITIAL_MANAGER_PASSWORD, "
                    "INITIAL_MANAGER_FIRST_NAME, INITIAL_MANAGER_LAST_NAME"
                )
            )
            # Optionally raise an error to stop startup if desired
            # raise ImproperlyConfigured("Missing superuser credentials in environment variables")
            return  # Or just exit gracefully

        # Create the superuser
        self.stdout.write(f"Creating manager '{first_name} {last_name}'...")
        try:
            User.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role=User.Role.MANAGER,
                is_staff=True,
            )
        except (IntegrityError, ValidationError) as exc:
            # Fail fast so deployments surface duplicate or invalid bootstrap accounts instead of hiding them.
            raise CommandError(f"Failed to create initial manager: {exc}") from exc
        else:
            self.stdout.write(self.style.SUCCESS(f"Manager '{first_name} {last_name}' created successfully."))
