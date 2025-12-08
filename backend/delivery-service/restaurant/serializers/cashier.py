from rest_framework import serializers
from restaurant.models import Order, OrderItem


class CashierOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "name", "quantity", "notes"]
        read_only_fields = fields


class CashierOrderSerializer(serializers.ModelSerializer):
    items = CashierOrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "created_at",
            "delivery_type",
            "status",
            "kitchen_status",
            "phone",
            "delivery_address",
            "items",
        ]
        read_only_fields = fields
