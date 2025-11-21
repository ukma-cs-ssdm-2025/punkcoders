from orders.models import Order
from orders.serializers.orders import OrderSerializer
from rest_framework import mixins, permissions, viewsets


class OrderViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Order.objects.select_related("user").prefetch_related("items__dish")
    serializer_class = OrderSerializer
    http_method_names = ["get", "post", "head", "options"]

    def get_permissions(self):
        """
        - create (POST) → AllowAny: може створити замовлення навіть гість
        - retrieve (GET) → IsAuthenticatedOrReadOnly (як у глобальних settings)
        """
        if self.action == "create":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticatedOrReadOnly()]
