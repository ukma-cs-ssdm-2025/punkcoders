from unittest.mock import patch

from accounts.models import User
from app.common_for_tests import find_failed_attr_in_err_response
from django.db.models import ProtectedError
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken

# A password that can be used in tests, clear to any reader
TEST_PASSWORD = "password123"  # nosec


class UserApiTests(APITestCase):
    """
    Integration tests for the User API endpoints:
    - /me/
    - /logout/
    - /users/
    - /users/<pk>/
    """

    def setUp(self):
        """Set up users with different roles for permission testing."""
        self.manager_user = User.objects.create_user(
            first_name="Manager",
            last_name="User",
            password=TEST_PASSWORD,
            email="manager@test.com",
            role=User.Role.MANAGER,
        )
        self.courier_user = User.objects.create_user(
            first_name="Courier",
            last_name="User",
            password=TEST_PASSWORD,
            email="courier@test.com",
            role=User.Role.COURIER,
        )
        self.kitchen_user = User.objects.create_user(
            first_name="Kitchen",
            last_name="User",
            password=TEST_PASSWORD,
            email="kitchen@test.com",
            role=User.Role.KITCHEN_STAFF,
        )

        # Define URLs
        self.self_user_url = reverse("self-user")
        self.logout_url = reverse("logout")
        self.user_list_url = reverse("user-list")

        # Detail URL for a non-manager user
        self.courier_detail_url = reverse("user-detail", args=[self.courier_user.id])
        # Detail URL for the manager (to test they can't manage themselves)
        self.manager_detail_url = reverse("user-detail", args=[self.manager_user.id])

    # --- /me/ (SelfUserView) Tests ---

    def test_get_self_user_fails_for_anonymous(self):
        """Test GET /me/ fails with 401 for unauthenticated users."""
        response = self.client.get(self.self_user_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_self_user_succeeds_for_authenticated(self):
        """Test GET /me/ succeeds for any authenticated user."""
        self.client.force_authenticate(user=self.courier_user)
        response = self.client.get(self.self_user_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.courier_user.email)
        self.assertEqual(response.data["role"], self.courier_user.role)

    def test_update_self_user_succeeds(self):
        """Test PATCH /me/ succeeds for updating first_name."""
        self.client.force_authenticate(user=self.courier_user)
        data = {"first_name": "Updated"}
        response = self.client.patch(self.self_user_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.courier_user.refresh_from_db()
        self.assertEqual(self.courier_user.first_name, "Updated")
        self.assertEqual(response.data["first_name"], "Updated")

    def test_update_self_user_password_succeeds(self):
        """Test PATCH /me/ succeeds for updating password."""
        self.client.force_authenticate(user=self.courier_user)
        data = {"password": "newpass123"}
        response = self.client.patch(self.self_user_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.courier_user.refresh_from_db()
        self.assertTrue(self.courier_user.check_password("newpass123"))
        self.assertFalse("password" in response.data, "Password should not be returned in response.")

    def test_update_self_user_role_fails(self):
        """Test PATCH /me/ ignores attempts to change the 'role'."""
        self.client.force_authenticate(user=self.courier_user)
        data = {"role": User.Role.MANAGER}
        response = self.client.patch(self.self_user_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.courier_user.refresh_from_db()
        # Role should be unchanged due to serializer's read_only=True
        self.assertEqual(self.courier_user.role, User.Role.COURIER)
        self.assertEqual(response.data["role"], User.Role.COURIER)

    # --- /logout/ (LogoutView) Tests ---

    def test_logout_fails_for_anonymous(self):
        """Test POST /logout/ fails with 401 for unauthenticated users."""
        response = self.client.post(self.logout_url, {"refresh": "faketoken"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_succeeds_for_authenticated(self):
        """Test POST /logout/ succeeds and blacklists the token."""
        refresh = RefreshToken.for_user(self.courier_user)
        token_str = str(refresh)

        self.client.force_authenticate(user=self.courier_user)
        response = self.client.post(self.logout_url, {"refresh": token_str})

        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
        self.assertTrue(
            BlacklistedToken.objects.filter(token__token=token_str).exists(), "Token should be in the blacklist."
        )

    def test_logout_fails_with_no_token(self):
        """Test POST /logout/ fails with 400 if no token is provided."""
        self.client.force_authenticate(user=self.courier_user)
        response = self.client.post(self.logout_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logout_fails_with_invalid_token(self):
        """Test POST /logout/ fails with 400 for an invalid token."""
        self.client.force_authenticate(user=self.courier_user)
        response = self.client.post(self.logout_url, {"refresh": "invalidtokenstring"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Token is invalid or expired.")

    # --- /users/ (UserViewSet) Permission Tests ---

    def test_user_list_fails_for_anonymous(self):
        """Test GET /users/ fails with 401 for unauthenticated users."""
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_list_fails_for_non_manager(self):
        """Test GET /users/ fails with 403 for non-manager (Courier) user."""
        self.client.force_authenticate(user=self.courier_user)
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_create_fails_for_non_manager(self):
        """Test POST /users/ fails with 403 for non-manager (Courier) user."""
        self.client.force_authenticate(user=self.courier_user)
        data = {"email": "a@b.com", "password": "abc", "first_name": "a", "last_name": "b", "role": "MANAGER"}
        response = self.client.post(self.user_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_update_fails_for_non_manager(self):
        """Test PATCH /users/<pk>/ fails with 403 for non-manager (Courier) user."""
        self.client.force_authenticate(user=self.courier_user)
        response = self.client.patch(self.courier_detail_url, {"role": "MANAGER"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # --- /users/ (UserViewSet) Manager Action Tests ---

    def test_manager_lists_users_excludes_self(self):
        """Test GET /users/ succeeds for Manager and excludes self."""
        self.client.force_authenticate(user=self.manager_user)
        response = self.client.get(self.user_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should list courier_user and kitchen_user (2)
        self.assertEqual(len(response.data), 2)

        emails_in_list = [u["email"] for u in response.data]
        self.assertIn(self.courier_user.email, emails_in_list)
        self.assertIn(self.kitchen_user.email, emails_in_list)
        self.assertNotIn(self.manager_user.email, emails_in_list, "Manager should not be in their own list.")

    def test_manager_cannot_retrieve_self(self):
        """Test GET /users/<manager_pk>/ fails (404) due to queryset exclusion."""
        self.client.force_authenticate(user=self.manager_user)
        response = self.client.get(self.manager_detail_url)
        # It's excluded from the queryset, so it's a 404
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_manager_create_user_succeeds(self):
        """Test POST /users/ succeeds for Manager."""
        self.client.force_authenticate(user=self.manager_user)
        data = {
            "email": "newuser@test.com",
            "first_name": "New",
            "last_name": "User",
            "password": "newpassword123",
            "role": User.Role.KITCHEN_STAFF,
        }
        self.assertEqual(User.objects.count(), 3)
        response = self.client.post(self.user_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 4)
        new_user = User.objects.get(email="newuser@test.com")
        self.assertEqual(new_user.role, User.Role.KITCHEN_STAFF)
        self.assertTrue(new_user.check_password("newpassword123"))

    def test_manager_create_user_fails_missing_data(self):
        """Test POST /users/ fails with 400 for missing required data."""
        self.client.force_authenticate(user=self.manager_user)
        data = {"email": "incomplete@test.com", "first_name": "Incomplete"}
        response = self.client.post(self.user_list_url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        find_failed_attr_in_err_response(response.data, "password")
        find_failed_attr_in_err_response(response.data, "last_name")
        find_failed_attr_in_err_response(response.data, "role")

    def test_manager_update_user_role_succeeds(self):
        """Test PATCH /users/<pk>/ succeeds for updating 'role'."""
        self.client.force_authenticate(user=self.manager_user)
        data = {"role": User.Role.KITCHEN_STAFF}
        response = self.client.patch(self.courier_detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.courier_user.refresh_from_db()
        self.assertEqual(self.courier_user.role, User.Role.KITCHEN_STAFF)
        self.assertEqual(response.data["role"], User.Role.KITCHEN_STAFF)

    def test_manager_update_user_read_only_fields_ignored(self):
        """Test PATCH /users/<pk>/ ignores read-only fields like 'email'."""
        self.client.force_authenticate(user=self.manager_user)
        data = {"email": "changed@test.com", "first_name": "Changed"}
        response = self.client.patch(self.courier_detail_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.courier_user.refresh_from_db()
        # Read-only fields should NOT change
        self.assertEqual(self.courier_user.email, "courier@test.com")
        self.assertEqual(self.courier_user.first_name, "Courier")
        self.assertEqual(response.data["email"], "courier@test.com")

    def test_manager_deactivate_user_succeeds_and_logs_out(self):
        """Test PATCH /users/<pk>/ to set is_active=False also blacklists tokens."""
        # 1. Create a token for the courier
        refresh = RefreshToken.for_user(self.courier_user)
        self.assertEqual(OutstandingToken.objects.filter(user=self.courier_user).count(), 1)
        token_db = OutstandingToken.objects.get(token=str(refresh))
        self.assertFalse(hasattr(token_db, "blacklistedtoken"), "Token should not be in the blacklist yet.")

        # 2. As manager, deactivate the courier
        self.client.force_authenticate(user=self.manager_user)
        data = {"is_active": False}
        response = self.client.patch(self.courier_detail_url, data)

        # 3. Check response and user status
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.courier_user.refresh_from_db()
        self.assertFalse(self.courier_user.is_active)
        self.assertFalse(response.data["is_active"])

        # 4. Check token was blacklisted
        token_db.refresh_from_db()
        self.assertTrue(hasattr(token_db, "blacklistedtoken"), "Token should be blacklisted on deactivation.")

    def test_manager_delete_user_succeeds(self):
        """Test DELETE /users/<pk>/ successfully deletes a user."""
        # We delete the kitchen_user, who has no relations
        self.client.force_authenticate(user=self.manager_user)
        kitchen_detail_url = reverse("user-detail", args=[self.kitchen_user.id])

        self.assertEqual(User.objects.count(), 3)
        response = self.client.delete(kitchen_detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 2)
        self.assertFalse(User.objects.filter(id=self.kitchen_user.id).exists())

    @patch("accounts.models.User.delete", side_effect=ProtectedError("Test ProtectedError", []))
    def test_manager_delete_user_with_relations_deactivates(self, mock_delete):
        """
        Test DELETE /users/<pk>/ deactivates user and blacklists tokens
        when a ProtectedError is raised.
        """
        # 1. Create a token for the courier
        refresh = RefreshToken.for_user(self.courier_user)
        self.assertEqual(OutstandingToken.objects.filter(user=self.courier_user).count(), 1)
        token_db = OutstandingToken.objects.get(token=str(refresh))

        # 2. As manager, attempt to delete the courier
        self.client.force_authenticate(user=self.manager_user)
        response = self.client.delete(self.courier_detail_url)

        # 3. Check response and user status
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.courier_user.refresh_from_db()
        self.assertFalse(self.courier_user.is_active, "User should be deactivated on ProtectedError.")

        # 4. Check token was blacklisted
        token_db.refresh_from_db()
        self.assertTrue(hasattr(token_db, "blacklistedtoken"), "Token should be blacklisted on failed delete.")

        # 5. Ensure delete was actually called
        mock_delete.assert_called_once()
