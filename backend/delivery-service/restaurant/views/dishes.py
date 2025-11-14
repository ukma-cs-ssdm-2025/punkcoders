from accounts.permissions import IsManager
from rest_framework import parsers, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from restaurant.models import Category, Dish, Ingredient
from restaurant.serializers.dishes import CategorySerializer, DishSerializer, IngredientSerializer
from restaurant.services.dishes import get_dishes_queryset


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Categories.
    - Managers can perform all CRUD operations.
    - All users (including anonymous) can list and retrieve categories.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    # явне сортування (узгоджене з Meta.ordering)
    queryset = Category.objects.all().order_by("name")
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

    queryset = Ingredient.objects.all().order_by("name")  # явне сортування
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

    queryset = (  # оптимізація запиту до бази, щоб не було помилки N+1
        Dish.objects.select_related("category").prefetch_related("ingredients").all()
    )

    serializer_class = DishSerializer
    # This is the key for file uploads. It tells DRF to expect multipart form data.
    # Accept JSON requests so API clients without file uploads are handled gracefully.
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsManager()]

    def get_queryset(self):
        """
        This is the magic part.
        This method overrides the default .queryset property.
        """
        # 1. Get the 'category_id' from the request's query parameters
        # e.g., /api/dishes/?category_id=1
        category_param = self.request.query_params.get("category_id")
        category_id = None
        if category_param is not None:
            try:
                category_id = int(category_param)
            except (TypeError, ValueError) as exc:
                # Reject malformed ids instead of letting the ORM raise ValueError deeper in the stack.
                raise ValidationError({"category_id": "Must be an integer."}) from exc
            if category_id < 1:
                # Ensure clients cannot query with invalid FK values that would return empty data silently.
                raise ValidationError({"category_id": "Must be a positive integer."})

        # 2. Call your service with the (optional) category_id
        return get_dishes_queryset(category_id=category_id)
