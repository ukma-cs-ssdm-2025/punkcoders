# accounts/test_models.py
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase

User = get_user_model()


class UserManagerTests(TestCase):

    def test_create_user_requires_role(self):
        with self.assertRaises((ValueError, IntegrityError)):
            User.objects.create_user(
                first_name="norole", last_name="user", email="a@a.a", password=settings.TEST_SECRET, role=None
            )

    def test_create_user_requires_email(self):
        """
        Tests that creating a user without an email raises a ValueError.
        """
        with self.assertRaises(ValueError):
            User.objects.create_user(
                first_name="noemail",
                last_name="user",
                email=None,
                password=settings.TEST_SECRET,
                role=User.Role.MANAGER,
            )

    def test_create_user_requires_first_name(self):
        """
        Tests that creating a user without a first name raises a ValueError.
        """
        with self.assertRaises(ValueError):
            User.objects.create_user(
                first_name=None, last_name="user", email="a@a.a", password=settings.TEST_SECRET, role=User.Role.MANAGER
            )

    def test_create_user_requires_last_name(self):
        """
        Tests that creating a user without a last name raises a ValueError.
        """
        with self.assertRaises(ValueError):
            User.objects.create_user(
                first_name="nolastname",
                last_name=None,
                email="a@a.a",
                password=settings.TEST_SECRET,
                role=User.Role.MANAGER,
            )

    def test_create_superuser_is_manager(self):
        """
        Tests that create_superuser() correctly sets the role to MANAGER
        and enables all required flags.
        """
        admin_user = User.objects.create_superuser(
            first_name="super", last_name="user", email="super@user.com", password=settings.TEST_SECRET
        )

        self.assertEqual(admin_user.role, User.Role.MANAGER)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_active)

    def test_create_superuser_raises_error_if_not_manager(self):
        """
        Tests that create_superuser() raises a ValueError if 'role' is
        forced to something other than MANAGER.
        """
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                first_name="super2",
                last_name="user",
                email="super2@user.com",
                password=settings.TEST_SECRET,
                role=User.Role.COURIER,  # Attempt to override
            )

    def test_create_superuser_raises_error_if_is_staff_false(self):
        """
        Tests that create_superuser() raises a ValueError if is_staff=False.
        """
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                first_name="super3",
                last_name="user",
                email="super3@user.com",
                password=settings.TEST_SECRET,
                is_staff=False,
            )
