from __future__ import annotations

from django.db import transaction
from django.shortcuts import get_object_or_404
from restaurant.models import Cart, CartItem, Dish


class CartError(Exception):
    """Base exception for cart errors."""


class CartItemNotFound(CartError):
    pass


class DishUnavailable(CartError):
    pass


@transaction.atomic
def add_item_to_cart(cart: Cart, dish_id: int, quantity: int) -> CartItem:
    dish = get_object_or_404(Dish, pk=dish_id)
    if not dish.is_available:
        raise DishUnavailable("Dish is not available for ordering.")

    cart_item, created = CartItem.objects.select_for_update().get_or_create(
        cart=cart,
        dish=dish,
        defaults={"quantity": 0, "unit_price": dish.price, "name": dish.name},
    )
    cart_item.quantity = cart_item.quantity + quantity
    cart_item.unit_price = dish.price
    cart_item.name = dish.name
    cart_item.save()
    return cart_item


@transaction.atomic
def set_item_quantity(cart: Cart, dish_id: int, quantity: int) -> CartItem | None:
    dish = get_object_or_404(Dish, pk=dish_id)
    if quantity <= 0:
        CartItem.objects.filter(cart=cart, dish=dish).delete()
        return None

    cart_item, created = CartItem.objects.select_for_update().get_or_create(
        cart=cart,
        dish=dish,
        defaults={"quantity": 0, "unit_price": dish.price, "name": dish.name},
    )
    cart_item.quantity = quantity
    cart_item.unit_price = dish.price
    cart_item.name = dish.name
    cart_item.save()
    return cart_item


@transaction.atomic
def remove_item_from_cart(cart: Cart, dish_id: int) -> None:
    deleted_count, _ = CartItem.objects.filter(cart=cart, dish_id=dish_id).delete()
    if deleted_count == 0:
        raise CartItemNotFound("Item not found in cart.")


@transaction.atomic
def clear_cart(cart: Cart) -> None:
    cart.items.all().delete()
