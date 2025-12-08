from accounts.permissions import IsCourier
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from restaurant.models import Order
from restaurant.serializers.courier import CourierOrderListSerializer, CourierOrderSerializer


class CourierOrderViewSet(viewsets.GenericViewSet):
    """
    ViewSet for courier operations on orders.

    Provides endpoints for:
    - Viewing ready orders (WAITING_FOR_COURIER)
    - Viewing own assigned deliveries (DELIVERING)
    - Assigning orders to self
    - Marking orders as delivered
    """

    permission_classes = [IsCourier]
    queryset = Order.objects.all().prefetch_related("items")

    def get_serializer_class(self):
        if self.action in ["ready", "my"]:
            return CourierOrderListSerializer
        return CourierOrderSerializer

    @action(detail=False, methods=["get"])
    def ready(self, request):
        """
        GET /courier/ready/
        Returns orders with status WAITING_FOR_COURIER that haven't been assigned.
        """
        orders = Order.objects.filter(
            status=Order.Status.WAITING_FOR_COURIER,
            courier__isnull=True,
            self_pickup=False,  # Only delivery orders
        ).order_by("created_at")

        serializer = CourierOrderListSerializer(orders, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def my(self, request):
        """
        GET /courier/my/
        Returns orders currently assigned to the logged-in courier.
        """
        orders = Order.objects.filter(
            courier=request.user,
            status=Order.Status.DELIVERING,
        ).order_by("-created_at")

        serializer = CourierOrderListSerializer(orders, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def details(self, request, pk=None):
        """
        GET /courier/{id}/details/
        Returns full order details including phone number for the courier.
        Only accessible for orders assigned to this courier or ready for pickup.
        """
        order = self.get_object()

        # Courier can only view details of:
        # 1. Orders assigned to them
        # 2. Orders waiting for courier (to check before assigning)
        if order.courier != request.user and order.status != Order.Status.WAITING_FOR_COURIER:
            return Response(
                {"detail": "Ви не можете переглядати це замовлення."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = CourierOrderSerializer(order)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def assign(self, request, pk=None):
        """
        POST /courier/{id}/assign/
        Assign an order to the current courier for delivery.
        """
        order = self.get_object()

        # Check if order is available for assignment
        if order.status != Order.Status.WAITING_FOR_COURIER:
            return Response(
                {"detail": "Це замовлення не готове до доставки."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if order.courier is not None:
            return Response(
                {"detail": "Це замовлення вже взяв інший кур'єр."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if order.self_pickup:
            return Response(
                {"detail": "Це замовлення на самовивіз."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Assign to current courier and update status
        order.courier = request.user
        order.status = Order.Status.DELIVERING
        order.save(update_fields=["courier", "status"])

        serializer = CourierOrderSerializer(order)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        """
        POST /courier/{id}/complete/
        Mark an order as delivered.
        Sets status to PAID_CASH or AWAITING_CASH based on payment method.
        """
        order = self.get_object()

        # Only the assigned courier can complete the order
        if order.courier != request.user:
            return Response(
                {"detail": "Це замовлення призначене іншому кур'єру."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if order.status != Order.Status.DELIVERING:
            return Response(
                {"detail": "Це замовлення не в процесі доставки."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Update status based on payment method
        if order.payment_method == Order.PaymentMethod.CREDIT:
            order.status = Order.Status.PAID_CREDIT
        else:
            # For cash payments, mark as paid (courier collected cash)
            order.status = Order.Status.PAID_CASH

        order.save(update_fields=["status"])

        serializer = CourierOrderSerializer(order)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def unassign(self, request, pk=None):
        """
        POST /courier/{id}/unassign/
        Remove assignment from an order (if courier can't deliver it).
        """
        order = self.get_object()

        if order.courier != request.user:
            return Response(
                {"detail": "Це замовлення призначене іншому кур'єру."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if order.status != Order.Status.DELIVERING:
            return Response(
                {"detail": "Це замовлення не можна повернути."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Return order to ready state
        order.courier = None
        order.status = Order.Status.WAITING_FOR_COURIER
        order.save(update_fields=["courier", "status"])

        return Response({"detail": "Замовлення повернуто в список готових."})
