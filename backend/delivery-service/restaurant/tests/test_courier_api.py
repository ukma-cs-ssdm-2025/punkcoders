from decimal import Decimal

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from restaurant.models import Category, Dish, Order, OrderItem

User = get_user_model()


class CourierApiTests(APITestCase):
    """Tests for courier delivery API endpoints."""

    @classmethod
    def setUpTestData(cls):
        # Create users with different roles
        cls.manager = User.objects.create_superuser(
            first_name="Manager",
            last_name="User",
            email="manager@example.com",
            password="password123",
        )
        cls.courier1 = User.objects.create_user(
            first_name="Courier",
            last_name="One",
            email="courier1@example.com",
            password="password123",
            role=User.Role.COURIER,
        )
        cls.courier2 = User.objects.create_user(
            first_name="Courier",
            last_name="Two",
            email="courier2@example.com",
            password="password123",
            role=User.Role.COURIER,
        )
        cls.kitchen_staff = User.objects.create_user(
            first_name="Kitchen",
            last_name="User",
            email="kitchen@example.com",
            password="password123",
            role=User.Role.KITCHEN_STAFF,
        )

        # Create test data
        cls.category = Category.objects.create(name="Pizza")
        cls.dish = Dish.objects.create(
            category=cls.category,
            name="Margherita",
            description="Classic pizza",
            price=Decimal("150.00"),
        )

        # Order ready for courier (WAITING_FOR_COURIER status)
        cls.order_ready = Order.objects.create(
            phone="+380501234567",
            delivery_address="вул. Шевченка 1, кв. 5",
            self_pickup=False,
            status=Order.Status.WAITING_FOR_COURIER,
            payment_method=Order.PaymentMethod.CASH,
        )
        OrderItem.objects.create(
            order=cls.order_ready,
            dish=cls.dish,
            name=cls.dish.name,
            unit_price=cls.dish.price,
            quantity=2,
            line_total=cls.dish.price * 2,
        )
        cls.order_ready.total_amount = Decimal("300.00")
        cls.order_ready.save(update_fields=["total_amount"])

        # Order being delivered by courier1
        cls.order_delivering = Order.objects.create(
            phone="+380501234568",
            delivery_address="вул. Франка 10",
            self_pickup=False,
            status=Order.Status.DELIVERING,
            courier=cls.courier1,
            payment_method=Order.PaymentMethod.CREDIT,
        )
        OrderItem.objects.create(
            order=cls.order_delivering,
            dish=cls.dish,
            name=cls.dish.name,
            unit_price=cls.dish.price,
            quantity=1,
            line_total=cls.dish.price,
        )
        cls.order_delivering.total_amount = Decimal("150.00")
        cls.order_delivering.save(update_fields=["total_amount"])

        # Self-pickup order (should not appear for couriers)
        cls.order_self_pickup = Order.objects.create(
            phone="+380501234569",
            self_pickup=True,
            status=Order.Status.WAITING_FOR_COURIER,
        )

    # ============= Access Control Tests =============

    def test_anonymous_cannot_access_courier_endpoints(self):
        """Anonymous users should get 401."""
        response = self.client.get("/api/v0/menu/courier/ready/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_kitchen_staff_cannot_access_courier_endpoints(self):
        """Non-courier roles should get 403."""
        self.client.force_authenticate(user=self.kitchen_staff)
        response = self.client.get("/api/v0/menu/courier/ready/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_courier_can_access_endpoints(self):
        """Couriers should have access."""
        self.client.force_authenticate(user=self.courier1)
        response = self.client.get("/api/v0/menu/courier/ready/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # ============= Ready Orders Tests =============

    def test_ready_orders_list(self):
        """Test listing orders ready for delivery."""
        self.client.force_authenticate(user=self.courier1)
        response = self.client.get("/api/v0/menu/courier/ready/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        ids = [order["id"] for order in response.data]
        # Should include order_ready but not self-pickup or already assigned
        self.assertIn(self.order_ready.id, ids)
        self.assertNotIn(self.order_self_pickup.id, ids)
        self.assertNotIn(self.order_delivering.id, ids)

    def test_ready_orders_include_address_and_amount(self):
        """Ready orders should show address and total amount."""
        self.client.force_authenticate(user=self.courier1)
        response = self.client.get("/api/v0/menu/courier/ready/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        order = next(o for o in response.data if o["id"] == self.order_ready.id)
        self.assertEqual(order["delivery_address"], "вул. Шевченка 1, кв. 5")
        self.assertEqual(Decimal(order["total_amount"]), Decimal("300.00"))

    # ============= My Orders Tests =============

    def test_my_orders_list(self):
        """Test listing courier's current deliveries."""
        self.client.force_authenticate(user=self.courier1)
        response = self.client.get("/api/v0/menu/courier/my/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        ids = [order["id"] for order in response.data]
        self.assertIn(self.order_delivering.id, ids)
        self.assertNotIn(self.order_ready.id, ids)

    def test_my_orders_empty_for_new_courier(self):
        """Courier with no assigned orders should see empty list."""
        self.client.force_authenticate(user=self.courier2)
        response = self.client.get("/api/v0/menu/courier/my/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    # ============= Order Details Tests =============

    def test_order_details_includes_phone(self):
        """Courier can see phone number in order details."""
        self.client.force_authenticate(user=self.courier1)
        response = self.client.get(f"/api/v0/menu/courier/{self.order_delivering.id}/details/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["phone"], "+380501234568")
        self.assertIn("items", response.data)

    def test_order_details_accessible_for_ready_order(self):
        """Courier can view details of ready orders (before assigning)."""
        self.client.force_authenticate(user=self.courier1)
        response = self.client.get(f"/api/v0/menu/courier/{self.order_ready.id}/details/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_details_forbidden_for_other_couriers_active_order(self):
        """Courier cannot view details of orders assigned to others."""
        self.client.force_authenticate(user=self.courier2)
        response = self.client.get(f"/api/v0/menu/courier/{self.order_delivering.id}/details/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ============= Assign Order Tests =============

    def test_assign_order_success(self):
        """Courier can assign a ready order to themselves."""
        self.client.force_authenticate(user=self.courier1)
        response = self.client.post(f"/api/v0/menu/courier/{self.order_ready.id}/assign/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.order_ready.refresh_from_db()
        self.assertEqual(self.order_ready.courier, self.courier1)
        self.assertEqual(self.order_ready.status, Order.Status.DELIVERING)

    def test_assign_already_assigned_order_fails(self):
        """Cannot assign an order that's already being delivered."""
        self.client.force_authenticate(user=self.courier2)
        response = self.client.post(f"/api/v0/menu/courier/{self.order_delivering.id}/assign/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_assign_self_pickup_order_fails(self):
        """Cannot assign a self-pickup order."""
        self.client.force_authenticate(user=self.courier1)
        response = self.client.post(f"/api/v0/menu/courier/{self.order_self_pickup.id}/assign/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # ============= Complete Order Tests =============

    def test_complete_order_cash_payment(self):
        """Completing a cash order sets status to PAID_CASH."""
        # Create new order for this test
        order = Order.objects.create(
            phone="+380501111111",
            delivery_address="Test address",
            self_pickup=False,
            status=Order.Status.DELIVERING,
            courier=self.courier1,
            payment_method=Order.PaymentMethod.CASH,
            total_amount=Decimal("100.00"),
        )

        self.client.force_authenticate(user=self.courier1)
        response = self.client.post(f"/api/v0/menu/courier/{order.id}/complete/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        order.refresh_from_db()
        self.assertEqual(order.status, Order.Status.PAID_CASH)

    def test_complete_order_credit_payment(self):
        """Completing a credit order sets status to PAID_CREDIT."""
        self.client.force_authenticate(user=self.courier1)
        response = self.client.post(f"/api/v0/menu/courier/{self.order_delivering.id}/complete/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.order_delivering.refresh_from_db()
        self.assertEqual(self.order_delivering.status, Order.Status.PAID_CREDIT)

    def test_complete_order_by_wrong_courier_fails(self):
        """Courier cannot complete another courier's order."""
        self.client.force_authenticate(user=self.courier2)
        response = self.client.post(f"/api/v0/menu/courier/{self.order_delivering.id}/complete/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ============= Unassign Order Tests =============

    def test_unassign_order_success(self):
        """Courier can return an order to the ready list."""
        # Create order for this test
        order = Order.objects.create(
            phone="+380502222222",
            delivery_address="Another address",
            self_pickup=False,
            status=Order.Status.DELIVERING,
            courier=self.courier1,
            total_amount=Decimal("200.00"),
        )

        self.client.force_authenticate(user=self.courier1)
        response = self.client.post(f"/api/v0/menu/courier/{order.id}/unassign/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        order.refresh_from_db()
        self.assertIsNone(order.courier)
        self.assertEqual(order.status, Order.Status.WAITING_FOR_COURIER)

    def test_unassign_by_wrong_courier_fails(self):
        """Courier cannot unassign another courier's order."""
        self.client.force_authenticate(user=self.courier2)
        response = self.client.post(f"/api/v0/menu/courier/{self.order_delivering.id}/unassign/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
