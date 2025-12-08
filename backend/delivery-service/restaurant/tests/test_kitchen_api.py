from decimal import Decimal

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from restaurant.models import Category, Dish, Order, OrderItem

User = get_user_model()


class KitchenOrderApiTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.manager = User.objects.create_superuser(
            first_name="Manager",
            last_name="User",
            email="manager@example.com",
            password="password123",
        )
        cls.kitchen_staff = User.objects.create_user(
            first_name="Kitchen",
            last_name="User",
            email="kitchen@example.com",
            password="password123",
            role=User.Role.KITCHEN_STAFF,
        )
        cls.courier = User.objects.create_user(
            first_name="Courier",
            last_name="User",
            email="courier@example.com",
            password="password123",
            role=User.Role.COURIER,
        )

        cls.category = Category.objects.create(name="Pizza")
        cls.dish = Dish.objects.create(
            category=cls.category,
            name="Margherita",
            description="Classic",
            price=Decimal("120.00"),
        )

        cls.order_new = Order.objects.create(
            phone="+380501234567",
            delivery_address="Street 1",
            self_pickup=False,
            status=Order.Status.NEW,
            kitchen_status=Order.KitchenStatus.NEW,
        )
        OrderItem.objects.create(
            order=cls.order_new,
            dish=cls.dish,
            name=cls.dish.name,
            unit_price=cls.dish.price,
            quantity=1,
            line_total=cls.dish.price,
            notes="Без цибулі",
        )
        cls.order_new.total_amount = cls.order_new.items.first().line_total
        cls.order_new.save(update_fields=["total_amount"])

        cls.order_preparing = Order.objects.create(
            phone="+380501234568",
            delivery_address="Street 2",
            self_pickup=True,
            status=Order.Status.IN_PROGRESS,
            kitchen_status=Order.KitchenStatus.PREPARING,
        )
        OrderItem.objects.create(
            order=cls.order_preparing,
            dish=cls.dish,
            name=cls.dish.name,
            unit_price=cls.dish.price,
            quantity=2,
            line_total=cls.dish.price * 2,
        )
        cls.order_preparing.total_amount = cls.order_preparing.items.first().line_total
        cls.order_preparing.save(update_fields=["total_amount"])

        cls.order_completed = Order.objects.create(
            phone="+380501234569",
            delivery_address="Street 3",
            self_pickup=False,
            status=Order.Status.IN_PROGRESS,
            kitchen_status=Order.KitchenStatus.COMPLETED,
        )
        OrderItem.objects.create(
            order=cls.order_completed,
            dish=cls.dish,
            name=cls.dish.name,
            unit_price=cls.dish.price,
            quantity=1,
            line_total=cls.dish.price,
        )
        cls.order_completed.total_amount = cls.order_completed.items.first().line_total
        cls.order_completed.save(update_fields=["total_amount"])

    def test_anonymous_cannot_access(self):
        response = self.client.get("/api/v0/kitchen/orders/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_non_kitchen_role_forbidden(self):
        self.client.force_authenticate(user=self.courier)
        response = self.client.get("/api/v0/kitchen/orders/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_active_orders(self):
        self.client.force_authenticate(user=self.kitchen_staff)
        response = self.client.get("/api/v0/kitchen/orders/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = {order["id"] for order in response.data}
        self.assertIn(self.order_new.id, ids)
        self.assertIn(self.order_preparing.id, ids)
        self.assertNotIn(self.order_completed.id, ids)

        new_order = next(order for order in response.data if order["id"] == self.order_new.id)
        self.assertEqual(new_order["dishes"][0]["notes"], "Без цибулі")

    def test_start_preparing_flow(self):
        self.client.force_authenticate(user=self.manager)
        url = f"/api/v0/kitchen/orders/{self.order_new.id}/start/"
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order_new.refresh_from_db()
        self.assertEqual(self.order_new.kitchen_status, Order.KitchenStatus.PREPARING)

    def test_complete_flow(self):
        self.client.force_authenticate(user=self.kitchen_staff)
        url = f"/api/v0/kitchen/orders/{self.order_preparing.id}/complete/"
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order_preparing.refresh_from_db()
        self.assertEqual(self.order_preparing.kitchen_status, Order.KitchenStatus.COMPLETED)

    def test_invalid_transition_rejected(self):
        self.client.force_authenticate(user=self.kitchen_staff)
        url = f"/api/v0/kitchen/orders/{self.order_new.id}/complete/"
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
