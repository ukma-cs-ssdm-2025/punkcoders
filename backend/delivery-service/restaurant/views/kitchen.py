from accounts.permissions import IsKitchenOrManager
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from restaurant.models import Order
from restaurant.serializers.orders import KitchenOrderSerializer


class KitchenOrderViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    ViewSet for kitchen staff to manage orders.

    Shows orders that need kitchen attention (NEW, IN_PROGRESS).
    Allows starting preparation and marking as ready for delivery.
    """

    queryset = Order.objects.all().prefetch_related("items")
    serializer_class = KitchenOrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsKitchenOrManager]

    def get_queryset(self):
        """
        Filter orders relevant to kitchen:
        - NEW: waiting to be prepared
        - IN_PROGRESS: currently being prepared
        Excludes orders already waiting for courier or beyond.
        """
        qs = super().get_queryset()
        # qs = qs.filter(kitchen_status__in=[Order.KitchenStatus.NEW, Order.KitchenStatus.PREPARING])
        qs = qs.filter(status__in=[Order.Status.NEW, Order.Status.IN_PROGRESS])
        return qs.order_by("created_at")

    @action(detail=True, methods=["post"], url_path="start")
    def start_preparing(self, request, *args, **kwargs):
        """
        POST /kitchen/orders/{id}/start/
        Mark order as being prepared (status: IN_PROGRESS).
        """
        order = self.get_object()
        if order.kitchen_status != Order.KitchenStatus.NEW:
            return Response(
                {"detail": "Це замовлення вже в обробці або завершене."}, status=status.HTTP_400_BAD_REQUEST
            )
        order.status = Order.Status.IN_PROGRESS
        order.kitchen_status = Order.KitchenStatus.PREPARING
        order.save(update_fields=["status", "kitchen_status"])
        return Response(self.get_serializer(order).data)

    @action(detail=True, methods=["post"], url_path="complete")
    def complete_order(self, request, *args, **kwargs):
        """
        POST /kitchen/orders/{id}/complete/
        Mark order as ready for delivery (status: WAITING_FOR_COURIER).
        For self-pickup orders, marks as paid immediately.
        """
        order = self.get_object()
        if order.kitchen_status != Order.KitchenStatus.PREPARING:
            return Response(
                {"detail": "Замовлення має бути 'в процесі' перед завершенням."}, status=status.HTTP_400_BAD_REQUEST
            )

        if order.self_pickup:
            order.status = Order.Status.AWAITING_CASH
        else:
            # Delivery: ready for courier
            order.status = Order.Status.WAITING_FOR_COURIER

        order.kitchen_status = Order.KitchenStatus.COMPLETED

        order.save(update_fields=["status", "kitchen_status"])
        return Response(self.get_serializer(order).data)
