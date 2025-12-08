from rest_framework import serializers
from restaurant.models import Order, OrderItem


class OrderItemCreateSerializer(serializers.Serializer):
    dish_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
    notes = serializers.CharField(required=False, allow_blank=True, max_length=255)


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "dish", "name", "unit_price", "quantity", "line_total", "notes"]
        read_only_fields = ["id", "dish", "name", "unit_price", "line_total", "notes"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    # input for items on creation (separate field)
    items_input = OrderItemCreateSerializer(many=True, write_only=True, required=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "status",
            "payment_method",
            "delivery_address",
            "self_pickup",
            "phone",
            "created_at",
            "updated_at",
            "total_amount",
            "items",
            "items_input",
        ]
        read_only_fields = ["id", "status", "created_at", "updated_at", "total_amount", "items"]

    def validate(self, data):
        # items_input present validated by serializer; additional checks:
        self_pickup = data.get("self_pickup", False)
        address = data.get("delivery_address")
        if self_pickup and address:
            raise serializers.ValidationError("If self_pickup is True, delivery_address must be empty.")
        if (not self_pickup) and (not address):
            raise serializers.ValidationError("Either delivery_address or self_pickup must be set.")
        return data

    def create(self, validated_data):
        items_data = validated_data.pop("items_input")
        # delegate to service to keep view thin
        from restaurant.services.orders import OrderCreationError, create_order_with_items

        try:
            order = create_order_with_items(validated_data, items_data)
        except OrderCreationError as e:
            raise serializers.ValidationError(str(e))
        return order

    def update(self, instance, validated_data):
        # forbid updating via serializer (policy from issue)
        raise serializers.ValidationError("Updating orders is not allowed via this endpoint.")


class KitchenOrderItemSerializer(serializers.ModelSerializer):
    qty = serializers.IntegerField(source="quantity")

    class Meta:
        model = OrderItem
        fields = ["id", "name", "qty", "notes"]
        read_only_fields = fields


class KitchenOrderSerializer(serializers.ModelSerializer):
    total_price = serializers.DecimalField(source="total_amount", max_digits=10, decimal_places=2)
    dishes = KitchenOrderItemSerializer(many=True, source="items", read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "status",
            "created_at",
            "self_pickup",
            "delivery_address",
            "total_price",
            "dishes",
        ]
        read_only_fields = fields
