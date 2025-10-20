import base64
import shutil
from pathlib import Path

from accounts.models import User
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from restaurant.models import Category

TEST_MEDIA_ROOT = Path(settings.BASE_DIR) / "test_media"


@override_settings(MEDIA_ROOT=str(TEST_MEDIA_ROOT))
class MenuApiTests(APITestCase):
    """
    Integration tests for the entire Menu API (Categories, Ingredients, Dishes).
    """

    @classmethod
    def setUpClass(cls):
        """
        This method runs once before any tests in this class.
        It creates the temporary media directory.
        """
        super().setUpClass()
        # We explicitly create the test_media directory
        TEST_MEDIA_ROOT.mkdir(parents=True, exist_ok=True)

    @classmethod
    def tearDownClass(cls):
        """
        This method runs once after all tests in this class are complete.
        It cleans up the temporary media directory and all its contents.
        """
        if TEST_MEDIA_ROOT.exists():
            shutil.rmtree(TEST_MEDIA_ROOT)
        super().tearDownClass()

    def setUp(self):
        """Set up users and initial data for all tests."""
        self.manager_user = User.objects.create_user(
            username="manager",
            password="password123",
            email="manager@delivery.com",
            role=User.Role.MANAGER,  # nosec
        )
        self.customer_user = User.objects.create_user(
            username="customer",
            password="password123",
            email="customer@delivery.com",
            role=User.Role.CUSTOMER,  # nosec
        )
        self.category = Category.objects.create(name="Test Category", slug="test-category")

        # URLs for the API endpoints
        self.categories_url = reverse("category-list")
        self.dishes_url = reverse("dish-list")

    def test_list_categories_is_public(self):
        """
        Tests that anyone can list categories without being logged in.
        """
        response = self.client.get(self.categories_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_category_fails_for_anonymous(self):
        """
        Tests that an unauthenticated user gets a 401 Unauthorized error.
        """
        response = self.client.post(self.categories_url, {"name": "New Category"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_category_fails_for_customer(self):
        """
        Tests that a logged-in customer gets a 403 Forbidden error.
        """
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.post(self.categories_url, {"name": "New Category"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_category_succeeds_for_manager(self):
        """
        Tests that a logged-in manager can successfully create a category.
        """
        self.client.force_authenticate(user=self.manager_user)
        response = self.client.post(self.categories_url, {"name": "New Category"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)  # Initial + new one
        self.assertEqual(response.data["name"], "New Category")

    def test_create_dish_with_photo_upload(self):
        """
        Tests that a manager can create a dish and upload a photo using multipart/form-data.
        """
        self.client.force_authenticate(user=self.manager_user)
        # A minimal valid GIF image
        dummy_photo = SimpleUploadedFile(
            "photo.gif",
            base64.b64decode("R0lGODlhAQABAIAAAP///////yH5BAAAAAAALAAAAAABAAEAAAIBAAA="),
            content_type="image/gif",
        )
        dish_data = {
            "name": "Photo Dish",
            "description": "A dish with a photo upload.",
            "price": 15.99,
            "category_id": self.category.id,
            "photo": dummy_photo,
        }

        # When testing file uploads, you must specify format='multipart'
        response = self.client.post(self.dishes_url, data=dish_data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("photo", response.data)
        photo_url = response.data.get("photo")
        self.assertIsNotNone(photo_url)
        # This assumes your MEDIA_URL is correctly set up.
        self.assertIn("/dishes_photos/", photo_url)
        self.assertTrue(photo_url.endswith(".gif"))
