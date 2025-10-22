from accounts.permissions import IsManager
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from restaurant.serializers.dishes import DishSerializer
from restaurant.services.dishes import create_dish, delete_dish, get_dish_by_id, get_dishes, has_dish, update_dish

from .responses import RESPONSES


@extend_schema(tags=["Dishes"])
class DishViewSet(viewsets.ViewSet):
    """CRUD endpoints for Dishes."""

    serializer_class = DishSerializer

    def get_permissions(self):
        """
        Assigns permissions based on the action.
        - 'list' and 'retrieve' are open to anyone.
        - 'create', 'partial_update', 'destroy' require a manager.
        """
        if self.action in ["list", "retrieve"]:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated, IsManager]

        return [permission() for permission in permission_classes]

    @extend_schema(
        summary="List dishes",
        description="Return all dishes.",
        responses={
            200: DishSerializer(many=True),
            500: RESPONSES[500](),
        },
    )
    def list(self, request):
        data = get_dishes()
        serializer = DishSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Retrieve a dish by ID",
        responses={
            200: DishSerializer,
            404: RESPONSES[404]("Dish"),
            500: RESPONSES[500](),
        },
    )
    def retrieve(self, request, pk=None):
        if pk is None:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        data = get_dish_by_id(pk)
        if not data:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = DishSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary="Create a dish (Managers only)",
        responses={
            201: DishSerializer,
            400: RESPONSES[400](),
            401: RESPONSES[401](),
            403: RESPONSES[403](),
            500: RESPONSES[500](),
        },
    )
    def create(self, request):
        # The permission class handles the 401/403 check.
        # Now we just run the real logic.
        serializer = DishSerializer(data=request.data)
        if serializer.is_valid():
            data = create_dish(serializer.validated_data.copy())
            return Response(DishSerializer(data).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Update a dish (Managers only)",
        responses={
            200: DishSerializer,
            400: RESPONSES[400](),
            401: RESPONSES[401](),
            403: RESPONSES[403](),
            404: RESPONSES[404]("Dish"),
            500: RESPONSES[500](),
        },
    )
    def partial_update(self, request, pk=None):
        if pk is None or not has_dish(pk):
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = DishSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            data = update_dish(pk, serializer.validated_data.copy())
            return Response(DishSerializer(data).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Delete a dish (Managers only)",
        responses={
            204: RESPONSES[204]("Dish"),
            401: RESPONSES[401](),
            403: RESPONSES[403](),
            500: RESPONSES[500](),
        },
    )
    def destroy(self, request, pk=None):
        if pk is None or not has_dish(pk):
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        delete_dish(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
