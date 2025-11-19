from decimal import Decimal

from django.db import transaction

from ..models import Dish, Order, OrderItem


class OrderCreationError(Exception):
    pass


def create_order_with_items(order_data: dict, items_data: list, user=None) -> Order:
    """
    order_data: dict with keys: phone, delivery_address (optional), self_pickup (bool), payment_method (optional)
    items_data: list of dicts: {"dish_id": int, "quantity": int}
    Returns created Order instance.
    Raises OrderCreationError on validation issues.
    """
    if not items_data:
        raise OrderCreationError("Order must contain at least one item.")

    # Validate phone, address/self_pickup logic superficially here; model.clean will also enforce
    if not order_data.get("self_pickup") and not order_data.get("delivery_address"):
        raise OrderCreationError("Either delivery_address must be provided or self_pickup must be True.")
    if order_data.get("self_pickup") and order_data.get("delivery_address"):
        raise OrderCreationError("If self_pickup is True, delivery_address must be empty.")

    with transaction.atomic():
        order = Order.objects.create(
            phone=order_data["phone"],
            delivery_address=order_data.get("delivery_address"),
            self_pickup=bool(order_data.get("self_pickup", False)),
            payment_method=order_data.get("payment_method", Order.PaymentMethod.CASH),
        )

        total = Decimal("0.00")
        # lock selected dishes to avoid race conditions (optional)
        dish_ids = [it["dish_id"] for it in items_data]
        dishes = Dish.objects.filter(id__in=dish_ids)
        dishes_map = {d.id: d for d in dishes}
        if len(dishes_map) != len(set(dish_ids)):
            missing = set(dish_ids) - set(dishes_map.keys())
            raise OrderCreationError(f"Some dishes not found: {missing}")

        for it in items_data:
            dish = dishes_map[it["dish_id"]]
            qty = int(it.get("quantity", 1))
            unit_price = dish.price  # snapshot current price
            line_total = (unit_price or Decimal("0.00")) * Decimal(qty)
            OrderItem.objects.create(
                order=order,
                dish=dish,
                name=dish.name,
                unit_price=unit_price,
                quantity=qty,
                line_total=line_total,
            )
            total += line_total

        order.total_amount = total
        order.save(update_fields=["total_amount"])

        # business rule: if self_pickup -> mark paid instantly
        order.mark_paid_if_self_pickup()

        return order
