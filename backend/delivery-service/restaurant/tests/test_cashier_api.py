from decimal import Decimal

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from restaurant.models import Category, Dish, Order, OrderItem

User = get_user_model()


class CashierApiTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.cashier = User.objects.create_user(
            first_name="Cashier",
            last_name="User",
            email="cashier@example.com",
            password="password123",
            role=User.Role.CASHIER,
        )
        cls.manager = User.objects.create_superuser(
            first_name="Manager",
            last_name="User",
            email="manager@example.com",
            password="password123",
        )

        cls.category = Category.objects.create(name="Salads")
        cls.dish = Dish.objects.create(
            category=cls.category,
            name="Greek Salad",
            description="Fresh",
            price=Decimal("90.00"),
        )

        # Ready pickup order (should appear)
        cls.ready_pickup = Order.objects.create(
            phone="+380501234560",
            delivery_address=None,
            self_pickup=True,
            delivery_type=Order.DeliveryType.PICKUP,
            kitchen_status=Order.KitchenStatus.COMPLETED,
            status=Order.Status.PAID_CASH,
        )
        OrderItem.objects.create(
            order=cls.ready_pickup,
            dish=cls.dish,
            name=cls.dish.name,
            unit_price=cls.dish.price,
            quantity=1,
            line_total=cls.dish.price,
        )
        cls.ready_pickup.total_amount = cls.dish.price
        cls.ready_pickup.save(update_fields=["total_amount"])

        # Pickup but still preparing (should be filtered out)
        cls.pickup_preparing = Order.objects.create(
            phone="+380501234561",
            delivery_address=None,
            self_pickup=True,
            delivery_type=Order.DeliveryType.PICKUP,
            kitchen_status=Order.KitchenStatus.PREPARING,
            status=Order.Status.IN_PROGRESS,
        )

        # Delivery order completed (should be filtered out)
        cls.delivery_completed = Order.objects.create(
            phone="+380501234562",
            delivery_address="Street 5",
            self_pickup=False,
            delivery_type=Order.DeliveryType.DELIVERY,
            kitchen_status=Order.KitchenStatus.COMPLETED,
            status=Order.Status.WAITING_FOR_COURIER,
        )

        # Already picked up (should not show)
        cls.already_picked = Order.objects.create(
            phone="+380501234563",
            delivery_address=None,
            self_pickup=True,
            delivery_type=Order.DeliveryType.PICKUP,
            kitchen_status=Order.KitchenStatus.COMPLETED,
            status=Order.Status.PICKED_UP,
        )

    def test_list_only_ready_pickup_orders(self):
        self.client.force_authenticate(user=self.cashier)
        response = self.client.get("/api/v0/cashier/orders/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = {order["id"] for order in response.data}
        self.assertSetEqual(ids, {self.ready_pickup.id})

        order_data = response.data[0]
        self.assertEqual(order_data["items"][0]["name"], self.dish.name)

    def test_only_cashier_can_access(self):
        self.client.force_authenticate(user=self.manager)
        response = self.client.get("/api/v0/cashier/orders/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_mark_picked_up_flow(self):
        self.client.force_authenticate(user=self.cashier)
        url = f"/api/v0/cashier/orders/{self.ready_pickup.id}/mark_picked_up/"

        first_response = self.client.post(url)
        self.assertEqual(first_response.status_code, status.HTTP_200_OK)
        self.ready_pickup.refresh_from_db()
        self.assertEqual(self.ready_pickup.status, Order.Status.PICKED_UP)

        # Idempotent second call
        second_response = self.client.post(url)
        self.assertEqual(second_response.status_code, status.HTTP_200_OK)

        list_response = self.client.get("/api/v0/cashier/orders/")
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        ids = {order["id"] for order in list_response.data}
        self.assertNotIn(self.ready_pickup.id, ids)
