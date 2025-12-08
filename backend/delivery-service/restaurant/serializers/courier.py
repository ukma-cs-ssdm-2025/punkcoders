from rest_framework import serializers
from restaurant.models import Order, OrderItem


class CourierOrderItemSerializer(serializers.ModelSerializer):
    """Simplified item serializer for courier view."""

    class Meta:
        model = OrderItem
        fields = ["id", "name", "quantity", "line_total"]


class CourierOrderSerializer(serializers.ModelSerializer):
    """
    Serializer for courier view of orders.
    Shows only information relevant for delivery.
    """

    items = CourierOrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "status",
            "delivery_address",
            "phone",
            "total_amount",
            "created_at",
            "payment_method",
            "items",
        ]
        read_only_fields = fields


class CourierOrderListSerializer(serializers.ModelSerializer):
    """
    Lighter serializer for list views (no items).
    Shows key info for courier to decide which orders to take.
    """

    class Meta:
        model = Order
        fields = [
            "id",
            "delivery_address",
            "total_amount",
            "created_at",
            "payment_method",
        ]
        read_only_fields = fields
