from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

User = get_user_model()


class SecurityTests(APITestCase):
    """
    Tests for security-related features of the accounts app,
    such as password hashing.
    """

    def test_password_is_hashed_with_argon2id(self):
        """
        Verify that a new user's password is hashed using the Argon2id algorithm.
        """
        # Create a user to inspect
        user = User.objects.create_user(
            username="hash_test_user",
            email="bogus@nunya.com",
            password="a_very_secure_password_123!",
            role=User.Role.CUSTOMER,
        )
        # The stored password string should start with the algorithm identifier.
        self.assertTrue(user.password.startswith("$argon2id$"))
