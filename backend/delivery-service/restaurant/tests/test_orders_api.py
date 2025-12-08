from decimal import Decimal

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from restaurant.models import Category, Dish, Order, OrderItem

User = get_user_model()


class OrderCreationApiTests(APITestCase):
    """Tests for order creation via the API."""

    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name="Pizza")
        cls.dish1 = Dish.objects.create(
            category=cls.category,
            name="Margherita",
            description="Classic pizza",
            price=Decimal("150.00"),
        )
        cls.dish2 = Dish.objects.create(
            category=cls.category,
            name="Pepperoni",
            description="Spicy pizza",
            price=Decimal("180.00"),
        )
        cls.unavailable_dish = Dish.objects.create(
            category=cls.category,
            name="Special Pizza",
            description="Limited edition",
            price=Decimal("250.00"),
            is_available=False,
        )

    # ============= Successful Order Creation =============

    def test_create_order_with_delivery(self):
        """Test creating a delivery order with valid data."""
        data = {
            "phone": "+380501234567",
            "delivery_address": "вул. Шевченка 1, кв. 5",
            "self_pickup": False,
            "payment_method": "cash",
            "items_input": [
                {"dish_id": self.dish1.id, "quantity": 2},
                {"dish_id": self.dish2.id, "quantity": 1},
            ],
        }
        response = self.client.post("/api/v0/menu/orders/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify order data
        order = Order.objects.get(id=response.data["id"])
        self.assertEqual(order.phone, "+380501234567")
        self.assertEqual(order.delivery_address, "вул. Шевченка 1, кв. 5")
        self.assertFalse(order.self_pickup)
        self.assertEqual(order.status, Order.Status.NEW)
        self.assertEqual(order.total_amount, Decimal("480.00"))  # 150*2 + 180*1

        # Verify items
        self.assertEqual(order.items.count(), 2)

    def test_create_order_with_self_pickup(self):
        """Test creating a self-pickup order."""
        data = {
            "phone": "+380501234567",
            "self_pickup": True,
            "payment_method": "credit",
            "items_input": [{"dish_id": self.dish1.id, "quantity": 1}],
        }
        response = self.client.post("/api/v0/menu/orders/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        order = Order.objects.get(id=response.data["id"])
        self.assertTrue(order.self_pickup)
        self.assertIsNone(order.delivery_address)
        # Note: current behavior marks self-pickup as PAID immediately
        # This may need adjustment based on business requirements

    def test_create_order_with_item_notes(self):
        """Test creating order with special notes on items."""
        data = {
            "phone": "+380501234567",
            "self_pickup": True,
            "items_input": [
                {"dish_id": self.dish1.id, "quantity": 1, "notes": "Без цибулі"},
            ],
        }
        response = self.client.post("/api/v0/menu/orders/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        order = Order.objects.get(id=response.data["id"])
        item = order.items.first()
        self.assertEqual(item.notes, "Без цибулі")

    # ============= Validation Errors =============

    def test_create_order_without_items_fails(self):
        """Order must have at least one item."""
        data = {
            "phone": "+380501234567",
            "self_pickup": True,
            "items_input": [],
        }
        response = self.client.post("/api/v0/menu/orders/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_without_phone_fails(self):
        """Phone number is required."""
        data = {
            "self_pickup": True,
            "items_input": [{"dish_id": self.dish1.id, "quantity": 1}],
        }
        response = self.client.post("/api/v0/menu/orders/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_invalid_phone_fails(self):
        """Phone number must match validation pattern."""
        data = {
            "phone": "invalid_phone",
            "self_pickup": True,
            "items_input": [{"dish_id": self.dish1.id, "quantity": 1}],
        }
        response = self.client.post("/api/v0/menu/orders/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_without_address_and_not_self_pickup_fails(self):
        """Must provide either delivery_address or self_pickup."""
        data = {
            "phone": "+380501234567",
            "self_pickup": False,
            "items_input": [{"dish_id": self.dish1.id, "quantity": 1}],
        }
        response = self.client.post("/api/v0/menu/orders/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_with_address_and_self_pickup_fails(self):
        """Cannot have both delivery_address and self_pickup."""
        data = {
            "phone": "+380501234567",
            "delivery_address": "Some address",
            "self_pickup": True,
            "items_input": [{"dish_id": self.dish1.id, "quantity": 1}],
        }
        response = self.client.post("/api/v0/menu/orders/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_with_nonexistent_dish_fails(self):
        """Cannot order dishes that don't exist."""
        data = {
            "phone": "+380501234567",
            "self_pickup": True,
            "items_input": [{"dish_id": 99999, "quantity": 1}],
        }
        response = self.client.post("/api/v0/menu/orders/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_with_zero_quantity_fails(self):
        """Quantity must be at least 1."""
        data = {
            "phone": "+380501234567",
            "self_pickup": True,
            "items_input": [{"dish_id": self.dish1.id, "quantity": 0}],
        }
        response = self.client.post("/api/v0/menu/orders/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # ============= Order Retrieval =============

    def test_retrieve_order_by_id(self):
        """Test getting order details by ID."""
        order = Order.objects.create(
            phone="+380501234567",
            self_pickup=True,
            status=Order.Status.NEW,
            total_amount=Decimal("150.00"),
        )
        OrderItem.objects.create(
            order=order,
            dish=self.dish1,
            name=self.dish1.name,
            unit_price=self.dish1.price,
            quantity=1,
            line_total=self.dish1.price,
        )

        response = self.client.get(f"/api/v0/menu/orders/{order.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], order.id)
        self.assertEqual(len(response.data["items"]), 1)

    def test_list_orders_by_phone(self):
        """Test filtering orders by phone number."""
        Order.objects.create(phone="+380501111111", self_pickup=True)
        Order.objects.create(phone="+380501111111", self_pickup=True)
        Order.objects.create(phone="+380502222222", self_pickup=True)

        response = self.client.get("/api/v0/menu/orders/", {"phone": "+380501111111"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    # ============= Update/Delete Prevention =============

    def test_update_order_not_allowed(self):
        """Orders cannot be updated via API."""
        order = Order.objects.create(phone="+380501234567", self_pickup=True)
        response = self.client.put(
            f"/api/v0/menu/orders/{order.id}/",
            {"phone": "+380509999999"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_order_not_allowed(self):
        """Orders cannot be deleted via API."""
        order = Order.objects.create(phone="+380501234567", self_pickup=True)
        response = self.client.delete(f"/api/v0/menu/orders/{order.id}/")
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class KitchenSelfPickupVisibilityTests(APITestCase):
    """Tests to verify kitchen staff can see self-pickup orders."""

    @classmethod
    def setUpTestData(cls):
        cls.kitchen_staff = User.objects.create_user(
            first_name="Kitchen",
            last_name="Staff",
            email="kitchen@test.com",
            password="password123",
            role=User.Role.KITCHEN_STAFF,
        )

        cls.category = Category.objects.create(name="Pizza")
        cls.dish = Dish.objects.create(
            category=cls.category,
            name="Margherita",
            description="Classic",
            price=Decimal("150.00"),
        )

        # Self-pickup order (kitchen should see this)
        cls.order_self_pickup = Order.objects.create(
            phone="+380501234567",
            self_pickup=True,
            status=Order.Status.NEW,
        )
        OrderItem.objects.create(
            order=cls.order_self_pickup,
            dish=cls.dish,
            name=cls.dish.name,
            unit_price=cls.dish.price,
            quantity=1,
            line_total=cls.dish.price,
        )

        # Delivery order (kitchen should see this too)
        cls.order_delivery = Order.objects.create(
            phone="+380501234568",
            delivery_address="Test address",
            self_pickup=False,
            status=Order.Status.NEW,
        )
        OrderItem.objects.create(
            order=cls.order_delivery,
            dish=cls.dish,
            name=cls.dish.name,
            unit_price=cls.dish.price,
            quantity=1,
            line_total=cls.dish.price,
        )

    def test_kitchen_sees_self_pickup_orders(self):
        """Kitchen staff should see self-pickup orders in their list."""
        self.client.force_authenticate(user=self.kitchen_staff)
        response = self.client.get("/api/v0/menu/kitchen/orders/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        order_ids = [order["id"] for order in response.data]
        self.assertIn(self.order_self_pickup.id, order_ids)

    def test_kitchen_sees_delivery_orders(self):
        """Kitchen staff should see delivery orders in their list."""
        self.client.force_authenticate(user=self.kitchen_staff)
        response = self.client.get("/api/v0/menu/kitchen/orders/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        order_ids = [order["id"] for order in response.data]
        self.assertIn(self.order_delivery.id, order_ids)
