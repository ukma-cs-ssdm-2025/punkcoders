# accounts/models.py
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager to handle role-based
    user creation.
    """

    def create_user(self, email, password, first_name, last_name, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError("The Email must be set")
        if not first_name:
            raise ValueError("The First Name must be set")
        if not last_name:
            raise ValueError("The Last Name must be set")

        email = self.normalize_email(email)

        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, first_name, last_name, **extra_fields):
        """
        Create and save a SuperUser.
        Forces the role to be MANAGER.
        """
        # Set all the superuser flags
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        # Explicitly set the role to MANAGER for superusers
        extra_fields.setdefault("role", User.Role.MANAGER)

        # --- Error checking to ensure our rules are met ---
        if extra_fields.get("role") != User.Role.MANAGER:
            raise ValueError("Superuser must have role of Manager.")
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        # We call our new create_user, which handles the password and saving
        return self.create_user(email, password, first_name, last_name, **extra_fields)


class User(AbstractUser):
    class Role(models.TextChoices):
        MANAGER = "MANAGER", "Manager"
        KITCHEN_STAFF = "KITCHEN_STAFF", "Kitchen Staff"
        COURIER = "COURIER", "Courier"

    username = None  # We are not using username
    USERNAME_FIELD = "email"
    role = models.CharField(max_length=20, choices=Role.choices)
    first_name = models.CharField(_("first name"), max_length=50, blank=False, null=False)
    last_name = models.CharField(_("last name"), max_length=50, blank=False, null=False)
    email = models.EmailField(_("email address"), unique=True)

    # This prompts for these fields during 'createsuperuser'
    REQUIRED_FIELDS = ["first_name", "last_name"]

    # --- This line hooks up our new manager ---
    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"
