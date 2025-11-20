from accounts.models import User
from accounts.services import log_user_out_everywhere
from django.test import TestCase
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken


class UserServicesTests(TestCase):
    """
    Tests for user-related service functions.
    """

    def setUp(self):
        """Set up a user for service tests."""
        self.user = User.objects.create_user(
            email="testuser@test.com",
            first_name="Test",
            last_name="User",
            password="password123",
            role=User.Role.COURIER,
        )

    def test_log_user_out_everywhere(self):
        """
        Test that all outstanding tokens for a user are blacklisted.
        """
        # Create two refresh tokens for the user
        refresh1 = RefreshToken.for_user(self.user)
        refresh2 = RefreshToken.for_user(self.user)
        token1_str = str(refresh1)
        token2_str = str(refresh2)

        # Check that they created outstanding tokens
        self.assertEqual(OutstandingToken.objects.filter(user=self.user).count(), 2)

        # Get the token objects from the DB
        token1_db = OutstandingToken.objects.get(token=token1_str)
        token2_db = OutstandingToken.objects.get(token=token2_str)

        # Ensure they are not blacklisted yet
        self.assertFalse(hasattr(token1_db, "blacklistedtoken"), "Token1 should not be blacklisted yet.")
        self.assertFalse(hasattr(token2_db, "blacklistedtoken"), "Token2 should not be blacklisted yet.")

        # Call the service function
        log_user_out_everywhere(self.user)

        # Refresh the token objects from the DB
        token1_db.refresh_from_db()
        token2_db.refresh_from_db()

        # Check that they are now blacklisted
        self.assertTrue(hasattr(token1_db, "blacklistedtoken"), "Token1 should be blacklisted on full logout.")
        self.assertTrue(hasattr(token2_db, "blacklistedtoken"), "Token2 should be blacklisted on full logout.")

        # Verify that trying to use them raises an error
        with self.assertRaises(TokenError):
            RefreshToken(token1_str).access_token

        with self.assertRaises(TokenError):
            RefreshToken(token2_str).access_token

    def test_log_user_out_no_tokens(self):
        """
        Test that the service function runs without error if the user has no tokens.
        """
        # User from setUp has no tokens created for them
        self.assertEqual(OutstandingToken.objects.filter(user=self.user).count(), 0)

        try:
            # This should run without raising an exception
            log_user_out_everywhere(self.user)
        except Exception as e:
            self.fail(f"log_user_out_everywhere raised an exception unexpectedly: {e}")

        self.assertEqual(OutstandingToken.objects.filter(user=self.user).count(), 0)
