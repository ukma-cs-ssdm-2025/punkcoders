from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from restaurant.serializers.cart import CartItemInputSerializer, CartSerializer
from restaurant.services.cart import (
    CartItemNotFound,
    DishUnavailable,
    add_item_to_cart,
    clear_cart,
    remove_item_from_cart,
    set_item_quantity,
)


class CartViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def _get_cart(self, request):
        if not request.session.session_key:
            request.session.save()
        from restaurant.models import Cart

        cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
        return cart

    def list(self, request):
        cart = self._get_cart(request)
        serializer = CartSerializer(cart, context={"request": request})
        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def add_item(self, request):
        serializer = CartItemInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = self._get_cart(request)
        try:
            add_item_to_cart(cart, serializer.validated_data["dish_id"], serializer.validated_data["quantity"])
        except DishUnavailable as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        refreshed = CartSerializer(cart, context={"request": request})
        return Response(refreshed.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"])
    def update_item(self, request):
        serializer = CartItemInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = self._get_cart(request)
        try:
            set_item_quantity(cart, serializer.validated_data["dish_id"], serializer.validated_data["quantity"])
        except DishUnavailable as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        refreshed = CartSerializer(cart, context={"request": request})
        return Response(refreshed.data)

    @action(detail=False, methods=["post"])
    def remove_item(self, request):
        serializer = CartItemInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = self._get_cart(request)
        try:
            remove_item_from_cart(cart, serializer.validated_data["dish_id"])
        except CartItemNotFound as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_404_NOT_FOUND)
        refreshed = CartSerializer(cart, context={"request": request})
        return Response(refreshed.data)

    @action(detail=False, methods=["post"])
    def clear(self, request):
        cart = self._get_cart(request)
        clear_cart(cart)
        refreshed = CartSerializer(cart, context={"request": request})
        return Response(refreshed.data)
