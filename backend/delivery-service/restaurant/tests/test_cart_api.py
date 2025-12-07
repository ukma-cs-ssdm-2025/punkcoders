from decimal import Decimal

from rest_framework import status
from rest_framework.test import APITestCase
from restaurant.models import Category, Dish


class CartApiTests(APITestCase):
    def setUp(self):
        category = Category.objects.create(name="Pizza")
        self.dish = Dish.objects.create(
            category=category,
            name="Margherita",
            description="Cheese pizza",
            price=Decimal("10.00"),
            is_available=True,
        )

    def test_cart_starts_empty(self):
        response = self.client.get("/api/v0/cart/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["items"], [])
        self.assertEqual(response.data["total_amount"], "0.00")

    def test_add_and_update_item(self):
        add_response = self.client.post(
            "/api/v0/cart/add_item/", {"dish_id": self.dish.id, "quantity": 2}, format="json"
        )
        self.assertEqual(add_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(add_response.data["items"][0]["quantity"], 2)

        update_response = self.client.post(
            "/api/v0/cart/update_item/", {"dish_id": self.dish.id, "quantity": 3}, format="json"
        )
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.data["items"][0]["quantity"], 3)
        self.assertEqual(update_response.data["total_amount"], "30.00")

    def test_remove_and_clear(self):
        self.client.post("/api/v0/cart/add_item/", {"dish_id": self.dish.id, "quantity": 1}, format="json")
        remove_response = self.client.post(
            "/api/v0/cart/remove_item/", {"dish_id": self.dish.id, "quantity": 1}, format="json"
        )
        self.assertEqual(remove_response.status_code, status.HTTP_200_OK)
        self.assertEqual(remove_response.data["items"], [])

        self.client.post("/api/v0/cart/add_item/", {"dish_id": self.dish.id, "quantity": 1}, format="json")
        clear_response = self.client.post("/api/v0/cart/clear/")
        self.assertEqual(clear_response.status_code, status.HTTP_200_OK)
        self.assertEqual(clear_response.data["items"], [])
        self.assertEqual(clear_response.data["total_amount"], "0.00")
