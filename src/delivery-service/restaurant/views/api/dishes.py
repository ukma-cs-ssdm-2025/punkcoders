from rest_framework import viewsets, permissions
from restaurant.models import Dish
from restaurant.serializers.dishes import DishSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(tags=["Dishes"])
class DishViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only endpoints для Dish (list/retrieve), дані з БД.
    POST/PUT/PATCH/DELETE відсутні -> 405.
    """
    queryset = Dish.objects.all().order_by("id")
    serializer_class = DishSerializer
    permission_classes = [permissions.AllowAny]
