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
    photo = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Dish
        fields = [
            "id",
            "name",
            "description",
            "price",
            "photo",
            "is_available",
            "category",
            "category_id",
            "ingredients",
            "ingredients_data",  # For writing only
        ]

    def create(self, validated_data):
        """
        This is the new, correct place to call the service.
        DRF's ModelViewSet calls serializer.save(), which in turn calls this method.
        """
        # print("\n\nIn DishViewSet.create with data:", validated_data)
        # pdb.set_trace()
        dish = create_dish(validated_data)
        # print("Created dish:", dish)
        # print("\n\n")
        return dish

    def update(self, instance, validated_data):
        """
        This is the new, correct place to call the update service.
        """
        return update_dish(instance, validated_data)
