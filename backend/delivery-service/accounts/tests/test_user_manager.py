# accounts/test_models.py
from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class UserManagerTests(TestCase):

    def test_create_user_defaults_to_customer(self):
        """
        Tests that create_user() correctly sets the default role to CUSTOMER.
        """
        user = User.objects.create_user(username="testuser", email="normal@user.com", password="foo")

        self.assertEqual(user.role, User.Role.CUSTOMER)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_create_user_requires_email(self):
        """
        Tests that creating a user without an email raises a ValueError.
        """
        with self.assertRaises(ValueError):
            User.objects.create_user(username="noemail", email=None, password="foo")

    def test_create_superuser_is_manager(self):
        """
        Tests that create_superuser() correctly sets the role to MANAGER
        and enables all required flags.
        """
        admin_user = User.objects.create_superuser(username="super", email="super@user.com", password="foo")

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
                username="super2",
                email="super2@user.com",
                password="foo",
                role=User.Role.CUSTOMER,  # Attempt to override
            )

    def test_create_superuser_raises_error_if_is_staff_false(self):
        """
        Tests that create_superuser() raises a ValueError if is_staff=False.
        """
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                username="super3",
                email="super3@user.com",
                password="foo",
                is_staff=False,
            )
