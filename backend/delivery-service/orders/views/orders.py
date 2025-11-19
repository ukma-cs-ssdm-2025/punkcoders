from orders.models import Order
from orders.serializers.orders import OrderSerializer
from rest_framework import mixins, viewsets


class OrderViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Order.objects.select_related("user").prefetch_related("items__dish")
    serializer_class = OrderSerializer
    http_method_names = ["get", "post", "head", "options"]
