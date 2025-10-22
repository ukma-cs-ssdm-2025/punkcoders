# accounts/models.py
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager to handle role-based
    user creation.
    """

    def create_user(self, username, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        Defaults the role to CUSTOMER.
        """
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)

        # --- This handles Requirement 1 ---
        # Set default role if not provided
        extra_fields.setdefault("role", User.Role.CUSTOMER)

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        """
        Create and save a SuperUser.
        Forces the role to be MANAGER.
        """
        # Set all the superuser flags
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        # --- This handles Requirement 3 ---
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
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    class Role(models.TextChoices):
        MANAGER = "MANAGER", "Manager"
        CUSTOMER = "CUSTOMER", "Customer"
        # You can still add more roles here later

    role = models.CharField(max_length=20, choices=Role.choices)

    # --- This line hooks up our new manager ---
    objects = CustomUserManager()
