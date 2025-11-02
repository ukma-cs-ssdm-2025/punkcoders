from rest_framework import serializers
from restaurant.models import Category, Dish, DishIngredient, Ingredient
from restaurant.services.dishes import create_dish, update_dish


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.
    """

    class Meta:
        model = Category
        fields = ["id", "name", "slug"]
        read_only_fields = ["slug"]


class IngredientSerializer(serializers.ModelSerializer):
    """
    Serializer for the Ingredient model.
    """

    class Meta:
        model = Ingredient
        fields = ["id", "name"]


class DishIngredientSerializer(serializers.ModelSerializer):
    """
    Serializer for reading the ingredients related to a dish.
    """

    name = serializers.CharField(source="ingredient.name", read_only=True)
    ingredient_id = serializers.IntegerField(source="ingredient.id", read_only=True)

    class Meta:
        model = DishIngredient
        fields = ["ingredient_id", "name", "is_base_ingredient"]


# A simple serializer for the ingredient data we expect on write operations
class IngredientDataSerializer(serializers.Serializer):
    ingredient_id = serializers.IntegerField()
    is_base_ingredient = serializers.BooleanField(default=True)


class DishSerializer(serializers.ModelSerializer):
    """
    The main serializer for the Dish model. Handles reading, writing, and file uploads.
    """

    # --- For Reading ---
    category = CategorySerializer(read_only=True)
    ingredients = DishIngredientSerializer(source="dishingredient_set", many=True, read_only=True)

    # --- For Writing ---
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )
    # This field accepts a list of ingredients when creating/updating a dish.
    # It is not part of the model, so it's write_only.
    ingredients_data = IngredientDataSerializer(many=True, write_only=True, required=False)

    # This field handles the actual image file upload.
    photo = serializers.ImageField(required=False, allow_null=True, write_only=True)
    # and this the image download
    photo_url = serializers.SerializerMethodField()

    is_available = serializers.BooleanField(default=True, required=False)

    class Meta:
        model = Dish
        fields = [
            "id",
            "name",
            "description",
            "price",
            "photo",
            "photo_url",
            "is_available",
            "category",
            "category_id",
            "ingredients",
            "ingredients_data",
        ]

    def get_photo_url(self, obj):
        """
        Returns the absolute URL for the dish photo, or None if no photo exists.
        """
        if not obj.photo:
            return None
        request = self.context.get("request")
        if request:
            return request.build_absolute_uri(obj.photo.url)
        return obj.photo.url

    def create(self, validated_data):
        """
        This is the new, correct place to call the service.
        DRF's ModelViewSet calls serializer.save(), which in turn calls this method.
        """
        dish = create_dish(validated_data)
        return dish

    def update(self, instance, validated_data):
        """
        This is the new, correct place to call the update service.
        """
        return update_dish(instance, validated_data)
