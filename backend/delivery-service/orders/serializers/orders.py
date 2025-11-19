from collections import Counter

from accounts.models import User
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
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source="user")
    items = OrderItemSerializer(many=True, read_only=True)
    dishes = serializers.ListField(child=serializers.IntegerField(min_value=1), write_only=True)

    class Meta:
        model = Order
        fields = ["id", "user_id", "status", "total_price", "items", "dishes", "created_at", "updated_at"]
        read_only_fields = ["status", "total_price", "items", "created_at", "updated_at"]

    def create(self, validated_data):
        dish_ids = validated_data.pop("dishes", [])

        if not dish_ids:
            raise serializers.ValidationError({"dishes": "Add at least one dish id to create an order."})

        unique_ids = set(dish_ids)
        dishes = Dish.objects.filter(is_available=True, id__in=unique_ids)
        found_ids = set(dishes.values_list("id", flat=True))
        missing_ids = sorted(unique_ids - found_ids)
        if missing_ids:
            raise serializers.ValidationError(
                {"dishes": f"Unknown or unavailable dish ids: {', '.join(map(str, missing_ids))}."}
            )

        dish_map = {dish.id: dish for dish in dishes}
        items_data = [
            {"dish": dish_map[dish_id], "quantity": quantity} for dish_id, quantity in Counter(dish_ids).items()
        ]
        validated_data["items_data"] = items_data
        return create_order(validated_data)
