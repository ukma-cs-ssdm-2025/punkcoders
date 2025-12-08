from accounts.permissions import IsCashier
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from restaurant.models import Order
from restaurant.serializers.cashier import CashierOrderSerializer


class CashierOrderViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = CashierOrderSerializer
    permission_classes = [IsCashier]
    queryset = Order.objects.all().prefetch_related("items")

    def get_queryset(self):
        qs = super().get_queryset()

        # ЦЕ — для списку на дашборді касира
        if self.action == "list":
            return (
                qs.filter(
                    delivery_type=Order.DeliveryType.PICKUP,
                    kitchen_status=Order.KitchenStatus.COMPLETED,
                )
                .exclude(status=Order.Status.PICKED_UP)
                .order_by("created_at")
            )
        return qs

    @action(detail=True, methods=["post"], url_path="mark_picked_up")
    def mark_picked_up(self, request, *args, **kwargs):
        order = self.get_object()

        if order.delivery_type != Order.DeliveryType.PICKUP:
            return Response(
                {"detail": "Це не замовлення на самовивіз."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if order.kitchen_status != Order.KitchenStatus.COMPLETED:
            return Response(
                {"detail": "Замовлення ще не готове."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if order.status != Order.Status.PICKED_UP:
            order.status = Order.Status.PICKED_UP
            order.save(update_fields=["status"])

        serializer = self.get_serializer(order)
        return Response(serializer.data)
