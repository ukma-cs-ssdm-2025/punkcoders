from accounts.permissions import IsKitchenOrManager
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from restaurant.models import Order
from restaurant.serializers.orders import KitchenOrderSerializer


class KitchenOrderViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Order.objects.all().prefetch_related("items")
    serializer_class = KitchenOrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsKitchenOrManager]

    def get_queryset(self):
        qs = super().get_queryset()
        include_completed = self.request.query_params.get("include_completed")
        if not include_completed:
            qs = qs.exclude(kitchen_status=Order.KitchenStatus.COMPLETED)
        return qs

    @action(detail=True, methods=["post"], url_path="start")
    def start_preparing(self, request, *args, **kwargs):
        order = self.get_object()
        if order.kitchen_status != Order.KitchenStatus.NEW:
            return Response({"detail": "Order is not in 'new' state."}, status=status.HTTP_400_BAD_REQUEST)
        order.kitchen_status = Order.KitchenStatus.PREPARING
        order.save(update_fields=["kitchen_status"])
        return Response(self.get_serializer(order).data)

    @action(detail=True, methods=["post"], url_path="complete")
    def complete_order(self, request, *args, **kwargs):
        order = self.get_object()
        if order.kitchen_status != Order.KitchenStatus.PREPARING:
            return Response(
                {"detail": "Order must be 'preparing' before completion."}, status=status.HTTP_400_BAD_REQUEST
            )
        order.kitchen_status = Order.KitchenStatus.COMPLETED
        order.save(update_fields=["kitchen_status"])
        return Response(self.get_serializer(order).data)
