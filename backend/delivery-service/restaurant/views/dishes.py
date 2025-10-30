from accounts.permissions import IsManager
from rest_framework import parsers, viewsets
from rest_framework.permissions import AllowAny
from restaurant.models import Category, Dish, Ingredient
from restaurant.serializers.dishes import CategorySerializer, DishSerializer, IngredientSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Categories.
    - Managers can perform all CRUD operations.
    - All users (including anonymous) can list and retrieve categories.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsManager()]


class IngredientViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Ingredients.
    - Managers can perform all CRUD operations.
    - All users (including anonymous) can list and retrieve ingredients.
    """

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsManager()]


class DishViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Dishes.
    - Handles file uploads for the dish photo.
    - Uses the service layer for create and update logic.
    """

    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    # This is the key for file uploads. It tells DRF to expect multipart form data.
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsManager()]
