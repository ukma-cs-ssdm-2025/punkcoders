from __future__ import annotations

from rest_framework import serializers
from restaurant.models import Cart, CartItem


class CartItemInputSerializer(serializers.Serializer):
    dish_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1, default=1)


class CartItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="dish.id", read_only=True)
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(source="dish.description", read_only=True)
    price = serializers.DecimalField(source="unit_price", max_digits=10, decimal_places=2, read_only=True)
    photo = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ["id", "name", "description", "price", "photo", "quantity", "line_total"]
        read_only_fields = fields

    def get_photo(self, obj: CartItem):
        request = self.context.get("request")
        if obj.dish.photo:
            url = obj.dish.photo.url
            return request.build_absolute_uri(url) if request else url
        return None


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_amount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "session_key", "items", "total_amount"]
        read_only_fields = ["id", "session_key", "items", "total_amount"]
