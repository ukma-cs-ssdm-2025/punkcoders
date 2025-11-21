from decimal import Decimal

from django.db import transaction
from orders.models import Order, OrderItem
from rest_framework.exceptions import ValidationError


def _validate_order_payload(items_data):
    if not isinstance(items_data, (list, tuple)):
        raise ValidationError({"items": "Expected a list of dishes."})
    if not items_data:
        raise ValidationError({"items": "Order must contain at least one dish."})

    seen_dish_ids = set()
    for index, item in enumerate(items_data):
        if not isinstance(item, dict):
            raise ValidationError({"items": f"Item {index} must be an object."})
        dish = item.get("dish")
        if dish is None:
            raise ValidationError({"items": f"Item {index} must include a dish."})
        if dish.id in seen_dish_ids:
            raise ValidationError({"items": f"Duplicate dish id {dish.id} is not allowed."})
        seen_dish_ids.add(dish.id)

        quantity = item.get("quantity", 1)
        if not isinstance(quantity, int):
            raise ValidationError({"items": f"Quantity for dish {dish.id} must be an integer."})
        if quantity < 1:
            raise ValidationError({"items": f"Quantity for dish {dish.id} must be at least 1."})


@transaction.atomic
def create_order(validated_data):
    items_data = validated_data.pop("items_data", [])
    _validate_order_payload(items_data)

    order = Order.objects.create(total_price=Decimal("0.00"), **validated_data)

    order_items = []
    running_total = Decimal("0.00")
    for item in items_data:
        dish = item["dish"]
        quantity = item.get("quantity", 1)
        unit_price = dish.price
        running_total += unit_price * quantity
        order_items.append(OrderItem(order=order, dish=dish, quantity=quantity, unit_price=unit_price))

    OrderItem.objects.bulk_create(order_items)
    Order.objects.filter(id=order.id).update(total_price=running_total)
    order.total_price = running_total
    return order
