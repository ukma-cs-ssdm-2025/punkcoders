from accounts.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from restaurant.models import Category, Dish, Ingredient
from restaurant.services.dishes import create_dish, update_dish


class DishServiceTests(TestCase):
    """
    Tests for the dish service functions. These tests operate directly
    on the service layer, bypassing the API views.
    """

    def setUp(self):
        """Set up initial data for all tests."""
        self.category = Category.objects.create(name="Appetizers", slug="appetizers")
        self.ingredient1 = Ingredient.objects.create(name="Cheese")
        self.ingredient2 = Ingredient.objects.create(name="Tomato")
        self.manager_user = User.objects.create_user(
            username="testmanager",
            password="password123",
            email="bogus@nunya.com",
            role=User.Role.MANAGER,  # nosec
        )

    def test_create_dish_simple(self):
        """Test creating a dish without any ingredients."""
        dish_data = {
            "name": "Simple Fries",
            "description": "Just plain fries.",
            "price": 4.99,
            "category": self.category,
            "is_available": True,
        }

        dish = create_dish(dish_data)

        self.assertIsNotNone(dish)
        self.assertEqual(Dish.objects.count(), 1)
        self.assertEqual(dish.name, "Simple Fries")
        self.assertEqual(dish.category, self.category)

    def test_create_dish_with_ingredients(self):
        """Test creating a dish with a list of ingredients."""
        dish_data = {
            "name": "Cheesy Fries",
            "description": "Fries with cheese.",
            "price": 6.99,
            "category": self.category,
            "is_available": True,
            "ingredients_data": [{"ingredient_id": self.ingredient1.id, "is_base_ingredient": True}],
        }

        dish = create_dish(dish_data)

        self.assertEqual(Dish.objects.count(), 1)
        self.assertEqual(dish.dishingredient_set.count(), 1)
        self.assertEqual(dish.dishingredient_set.first().ingredient, self.ingredient1)

    def test_update_dish_photo(self):
        """Test that a photo can be added to an existing dish."""
        # Create a dish first
        dish_data = {
            "name": "Fries to be Updated",
            "price": 5.00,
            "category": self.category,
        }
        dish = create_dish(dish_data)
        self.assertFalse(dish.photo)  # Ensure it starts with no photo

        # Now, create a dummy image file in memory
        dummy_photo = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")

        update_data = {
            "photo": dummy_photo,
        }

        updated_dish = update_dish(dish, update_data)

        self.assertTrue(updated_dish.photo)
        self.assertIn("test_image", updated_dish.photo.name)
