from collections import Counter

from orders.models import Order, OrderItem
from orders.services.orders import create_order
from rest_framework import serializers
from restaurant.models import Dish


class OrderItemSerializer(serializers.ModelSerializer):
    dish_id = serializers.IntegerField(source="dish.id", read_only=True)
    dish_name = serializers.CharField(source="dish.name", read_only=True)

    class Meta:
        model = OrderItem
        fields = ["dish_id", "dish_name", "quantity", "unit_price"]
        read_only_fields = fields


class OrderSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    guest_name = serializers.CharField(required=False, allow_blank=True)
    guest_phone = serializers.CharField(required=False, allow_blank=True)
    guest_address = serializers.CharField(required=False, allow_blank=True)

    items = OrderItemSerializer(many=True, read_only=True)
    dishes = serializers.ListField(child=serializers.IntegerField(min_value=1), write_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user_id",
            "guest_name",
            "guest_phone",
            "guest_address",
            "status",
            "total_price",
            "items",
            "dishes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["status", "total_price", "items", "created_at", "updated_at"]

    def create(self, validated_data):
        request = self.context.get("request")

        if request.user.is_authenticated:
            validated_data["user"] = request.user
        else:
            if not validated_data.get("guest_name") or not validated_data.get("guest_phone"):
                raise serializers.ValidationError("Guest orders require 'guest_name' and 'guest_phone'.")

        dish_ids = validated_data.pop("dishes", [])
        if not dish_ids:
            raise serializers.ValidationError({"dishes": "Add at least one dish id."})

        unique_ids = set(dish_ids)
        dishes = Dish.objects.filter(is_available=True, id__in=unique_ids)
        found_ids = set(dishes.values_list("id", flat=True))
        missing = sorted(unique_ids - found_ids)

        if missing:
            raise serializers.ValidationError(
                {"dishes": f"Unknown or unavailable dish ids: {', '.join(map(str, missing))}"}
            )

        dish_map = {dish.id: dish for dish in dishes}
        items_data = [
            {"dish": dish_map[dish_id], "quantity": quantity} for dish_id, quantity in Counter(dish_ids).items()
        ]
        validated_data["items_data"] = items_data
        return create_order(validated_data)
