from rest_framework import mixins, permissions, viewsets
from rest_framework.response import Response
from restaurant.models import Order
from restaurant.serializers.orders import OrderSerializer


class OrderViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Order.objects.all().prefetch_related("items")
    serializer_class = OrderSerializer
    permission_classes = [permissions.AllowAny]  # налаштуй під проект: IsAuthenticated або власний

    def get_queryset(self):
        qs = super().get_queryset()
        # optional: filter by phone query param
        phone = self.request.query_params.get("phone")
        if phone:
            qs = qs.filter(phone=phone)
        return qs

    # optionally override destroy/update to prevent accidental enabling
    def partial_update(self, request, *args, **kwargs):
        return Response({"detail": "Updating orders is not allowed."}, status=405)

    def update(self, request, *args, **kwargs):
        return Response({"detail": "Updating orders is not allowed."}, status=405)

    def destroy(self, request, *args, **kwargs):
        return Response({"detail": "Deleting orders is not allowed."}, status=405)
