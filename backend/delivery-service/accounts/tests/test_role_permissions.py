# accounts/test_api.py
from accounts.permissions import IsManager
from django.contrib.auth import get_user_model
from django.urls import path
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.test import APITestCase
from rest_framework.views import APIView

User = get_user_model()
LOGIN_URL = "/api/token/"


# --- 1. Create a dummy view for testing ---
# This view is protected by *both* IsAuthenticated and your custom IsManager
class ProtectedManagerView(APIView):
    permission_classes = [IsAuthenticated, IsManager]

    def get(self, request):
        return Response({"message": "You are a manager!"}, status=status.HTTP_200_OK)


# --- 2. Define temporary URLs just for this test ---
# This setup is clean because it doesn't rely on your project's main urls.py
urlpatterns = [
    path("protected-view/", ProtectedManagerView.as_view(), name="protected-view"),
]


# --- 3. Write the test case ---
class PermissionTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        # Create the users we'll need for testing
        cls.courier_user = User.objects.create_user(
            first_name="courier",
            last_name="user",
            email="courier@example.com",
            password="password123",
            role=User.Role.COURIER,
        )

        cls.manager_user = User.objects.create_superuser(
            first_name="manager",
            last_name="user",
            email="manager@example.com",
            password="password123",
        )

        cls.protected_url = "/protected-view/"

    def test_user_can_login_with_valid_credentials(self):
        response = self.client.post(
            LOGIN_URL,
            {"email": "courier@example.com", "first_name": "courier", "last_name": "user", "password": "password123"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_user_cannot_login_with_invalid_password(self):
        response = self.client.post(
            LOGIN_URL,
            {"email": "courier@example.com", "first_name": "courier", "last_name": "user", "password": "wrongpassword"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_anonymous_user_cannot_access_protected_view(self):
        """
        GET /protected-view/
        Tests that an unauthenticated user gets a 401 Unauthorized.
        """
        # We don't authenticate the client
        response = self.client.get(self.protected_url)

        # We override the ROOT_URLCONF to use our dummy URLs
        with self.settings(ROOT_URLCONF=__name__):
            response = self.client.get(self.protected_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_user_cannot_access_protected_view(self):
        """
        GET /protected-view/
        Tests that a logged-in COURIER gets a 403 Forbidden.
        """
        self.client.force_authenticate(user=self.courier_user)

        with self.settings(ROOT_URLCONF=__name__):
            response = self.client.get(self.protected_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_manager_user_can_access_protected_view(self):
        """
        GET /protected-view/
        Tests that a logged-in MANAGER gets a 200 OK.
        """
        # Log in as the manager
        self.client.force_authenticate(user=self.manager_user)

        with self.settings(ROOT_URLCONF=__name__):
            response = self.client.get(self.protected_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "You are a manager!")
