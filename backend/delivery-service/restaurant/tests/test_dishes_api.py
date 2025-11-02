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
from restaurant.models import Category, Dish
from restaurant.serializers.dishes import DishSerializer

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
        self.dish = Dish.objects.create(
            name="Test Dish",
            description="A dish for testing.",
            price=10.99,
            category=self.category,
        )

        # URLs for the API endpoints
        self.categories_url = reverse("category-list")
        self.dishes_url = reverse("dish-list")
        self.dish_detail_url = reverse("dish-detail", args=[self.dish.id])
        self.non_existent_dish_url = reverse("dish-detail", args=[9999])

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
        self.assertIn("slug", response.data)
        self.assertEqual(response.data["slug"], "new-category")

    def test_create_two_categories_succeeds_for_manager(self):
        """
        Tests that a logged-in manager can successfully create a category.
        """
        self.client.force_authenticate(user=self.manager_user)
        # this kinda assumes the previous test passed and this works properly
        self.client.post(self.categories_url, {"name": "New Category"})
        response = self.client.post(self.categories_url, {"name": "Another Category"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 3)  # Initial + new one + another
        self.assertEqual(response.data["name"], "Another Category")
        self.assertIn("slug", response.data)
        self.assertEqual(response.data["slug"], "another-category")

    def test_create_dish_fails_for_anonymous(self):
        """
        Tests that an unauthenticated user gets 401 on POST /api/dishes/.
        """
        dish_data = {
            "name": "New Dish",
            "price": 5.00,
            "category_id": self.category.id,
        }
        response = self.client.post(self.dishes_url, data=dish_data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_dish_fails_for_customer(self):
        """
        Tests that a customer user gets 403 on POST /api/dishes/.
        """
        self.client.force_authenticate(user=self.customer_user)
        dish_data = {
            "name": "New Dish",
            "price": 5.00,
            "category_id": self.category.id,
        }
        response = self.client.post(self.dishes_url, data=dish_data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_dish_succeeds_for_manager(self):
        """
        Tests that a manager can create a dish with JSON data.
        """
        self.client.force_authenticate(user=self.manager_user)
        dish_data = {
            "name": "New Dish by Manager",
            "description": "A new creation.",
            "price": 12.50,
            "category_id": self.category.id,
            # "is_available": True,
        }
        response = self.client.post(self.dishes_url, data=dish_data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Dish.objects.count(), 2)  # The setUp dish + this new one
        self.assertEqual(response.data["name"], "New Dish by Manager")
        self.assertEqual(float(response.data["price"]), 12.50)
        self.assertEqual(response.data["is_available"], True)  # Default value

    def test_create_unvailable_dish_succeeds_for_manager(self):
        """
        Tests that a manager can create a dish with JSON data.
        """
        self.client.force_authenticate(user=self.manager_user)
        dish_data = {
            "name": "New Dish by Manager",
            "description": "A new creation.",
            "price": 12.50,
            "category_id": self.category.id,
            "is_available": False,
        }
        response = self.client.post(self.dishes_url, data=dish_data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Dish.objects.count(), 2)  # The setUp dish + this new one
        self.assertEqual(response.data["name"], "New Dish by Manager")
        self.assertEqual(float(response.data["price"]), 12.50)
        self.assertEqual(response.data["is_available"], False)  # Default value

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
        self.assertIn("photo_url", response.data)
        photo_url = response.data.get("photo_url")
        self.assertIsNotNone(photo_url)
        self.assertIn("/dishes_photos/", photo_url)
        self.assertTrue(photo_url.endswith(".gif"))

    def test_list_dishes_is_public(self):
        """
        Tests that anyone can list dishes (GET /api/dishes/).
        """
        response = self.client.get(self.dishes_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # We created one dish in setUp
        self.assertEqual(len(response.data), 1)

    def test_retrieve_dish_is_public(self):
        """
        Tests that anyone can retrieve a single dish (GET /api/dishes/<id>/).
        """
        response = self.client.get(self.dish_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.dish.name)

    def test_full_update_dish_fails_for_anonymous(self):
        """
        Tests that an unauthenticated user gets 401 on PUT /api/dishes/<id>/.
        """
        update_data = {
            "name": "Full Update Name",
            "price": 99.99,
            "category_id": self.category.id,
        }
        response = self.client.put(self.dish_detail_url, data=update_data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_full_update_dish_fails_for_customer(self):
        """
        Tests that a customer user gets 403 on PUT /api/dishes/<id>/.
        """
        self.client.force_authenticate(user=self.customer_user)
        update_data = {
            "name": "Full Update Name",
            "price": 99.99,
            "category_id": self.category.id,
        }
        response = self.client.put(self.dish_detail_url, data=update_data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_full_update_dish_succeeds_for_manager(self):
        """
        Tests that a manager can fully replace a dish (PUT /api/dishes/<id>/).
        """
        self.client.force_authenticate(user=self.manager_user)

        # We must provide *all* required fields for a PUT
        update_data = {
            "name": "Fully Updated Dish",
            "description": "A completely new description.",
            "price": 99.99,
            "category_id": self.category.id,
            "is_available": False,
        }
        response = self.client.put(self.dish_detail_url, data=update_data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that all fields were updated
        self.dish.refresh_from_db()
        self.assertEqual(self.dish.name, "Fully Updated Dish")
        self.assertEqual(float(self.dish.price), 99.99)
        self.assertEqual(self.dish.category, self.category)
        self.assertFalse(self.dish.is_available)

    def test_full_update_dish_fails_if_missing_fields(self):
        """
        Tests that a PUT request fails with 400 if required fields are missing.
        """
        self.client.force_authenticate(user=self.manager_user)

        # This data is incomplete. A PUT requires all fields.
        # 'price' and 'category_id' are missing.
        update_data = {"name": "Incomplete Update"}

        response = self.client.put(self.dish_detail_url, data=update_data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check that the response contains errors for the missing fields
        self.assertIn("price", response.data)
        self.assertIn("category_id", response.data)

    def test_partial_update_dish_fails_for_anonymous(self):
        """
        Tests that an unauthenticated user gets 401 on PATCH /api/dishes/<id>/.
        """
        update_data = {"price": 99.99}
        response = self.client.patch(self.dish_detail_url, data=update_data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_partial_update_dish_fails_for_customer(self):
        """
        Tests that a customer user gets 403 on PATCH /api/dishes/<id>/.
        """
        self.client.force_authenticate(user=self.customer_user)
        update_data = {"price": 99.99}
        response = self.client.patch(self.dish_detail_url, data=update_data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_partial_update_dish_succeeds_for_manager(self):
        """
        Tests that a manager can partially update a dish (PATCH /api/dishes/<id>/).
        """
        self.client.force_authenticate(user=self.manager_user)
        update_data = {"price": 99.99}  # Only updating the price
        response = self.client.patch(self.dish_detail_url, data=update_data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh the dish from the database to check the change
        self.dish.refresh_from_db()
        self.assertEqual(float(self.dish.price), 99.99)
        # Check that the name (which wasn't sent) is unchanged
        self.assertEqual(self.dish.name, "Test Dish")

    def test_partial_update_dish_with_identical_data_succeeds_for_manager(self):
        """
        Tests that a manager can partially update a dish with identical data (PATCH /api/dishes/<id>/).
        """
        self.client.force_authenticate(user=self.manager_user)
        update_data = DishSerializer(self.dish).data  # Get current data
        update_data["category_id"] = update_data["category"]["id"]  # Adjust for write field
        del update_data["category"]  # Remove read-only field
        del update_data["photo_url"]  # ditto
        response = self.client.patch(self.dish_detail_url, data=update_data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh the dish from the database to check the change
        self.dish.refresh_from_db()
        self.assertEqual(self.dish.name, "Test Dish")  # Name should remain unchanged

    def test_delete_dish_fails_for_anonymous(self):
        """
        Tests that an unauthenticated user gets 401 on DELETE /api/dishes/<id>/.
        """
        response = self.client.delete(self.dish_detail_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_dish_fails_for_customer(self):
        """
        Tests that a customer user gets 403 on DELETE /api/dishes/<id>/.
        """
        self.client.force_authenticate(user=self.customer_user)
        response = self.client.delete(self.dish_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_dish_succeeds_for_manager(self):
        """
        Tests that a manager can delete a dish (DELETE /api/dishes/<id>/).
        """
        self.client.force_authenticate(user=self.manager_user)
        response = self.client.delete(self.dish_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check that the dish is actually gone from the database
        self.assertFalse(Dish.objects.filter(id=self.dish.id).exists())

    def test_retrieve_non_existent_dish_fails_404(self):
        """
        Tests that GET /api/dishes/9999/ returns a 404.
        """
        response = self.client.get(self.non_existent_dish_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_full_update_non_existent_dish_fails_404(self):
        """
        Tests that PUT /api/dishes/9999/ returns a 404.
        """
        self.client.force_authenticate(user=self.manager_user)
        update_data = {
            "name": "Full Update Name",
            "price": 99.99,
            "category_id": self.category.id,
        }
        response = self.client.put(self.non_existent_dish_url, data=update_data, format="multipart")
        # 404 should be returned even if authenticated
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_partial_update_non_existent_dish_fails_404(self):
        """
        Tests that PATCH /api/dishes/9999/ returns a 404.
        """
        self.client.force_authenticate(user=self.manager_user)
        update_data = {"price": 99.99}
        response = self.client.patch(self.non_existent_dish_url, data=update_data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_non_existent_dish_fails_404(self):
        """
        Tests that DELETE /api/dishes/9999/ returns a 404.
        """
        self.client.force_authenticate(user=self.manager_user)
        response = self.client.delete(self.non_existent_dish_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_dish_missing_required_fields_fails_400(self):
        """
        Tests that POST /api/dishes/ fails with 400 if required fields
        like 'name', 'price', or 'category_id' are missing.
        """
        self.client.force_authenticate(user=self.manager_user)
        # 'price' and 'category_id' are missing
        dish_data = {"name": "A Dish with No Price"}

        response = self.client.post(self.dishes_url, data=dish_data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("price", response.data)
        self.assertIn("category_id", response.data)

    def test_create_dish_with_invalid_category_id_fails_400(self):
        """
        Tests that POST /api/dishes/ fails with 400 if the 'category_id'
        provided does not exist.
        """
        self.client.force_authenticate(user=self.manager_user)
        dish_data = {
            "name": "New Dish by Manager",
            "price": 12.50,
            "category_id": 9999,  # Non-existent category
        }
        response = self.client.post(self.dishes_url, data=dish_data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Check for the specific error from the PrimaryKeyRelatedField
        self.assertIn("category_id", response.data)
        self.assertIn("does not exist", str(response.data["category_id"]))

    def test_create_dish_with_invalid_photo_fails_400(self):
        """
        Tests that uploading a non-image file to the 'photo' field fails.
        """
        self.client.force_authenticate(user=self.manager_user)

        # Create a dummy text file instead of an image
        # Pillow will shoot this down, beause API tests do run validators
        dummy_file = SimpleUploadedFile(
            "not_an_image.txt",
            b"This is just some text.",
            content_type="text/plain",
        )

        dish_data = {
            "name": "Bad Photo Dish",
            "price": 15.99,
            "category_id": self.category.id,
            "photo": dummy_file,
        }
        response = self.client.post(self.dishes_url, data=dish_data, format="multipart")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("photo", response.data)
        self.assertIn("Upload a valid image", str(response.data["photo"]))
