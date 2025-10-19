from rest_framework import serializers
from restaurant.models import Dish, Ingredient


class IngredientInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ["id", "name"]


class DishSerializer(serializers.ModelSerializer):
    # назва категорії як текст (read-only)
    category = serializers.CharField(source="category.name", read_only=True)
    # інгредієнти як масив об’єктів {id, name} (read-only)
    ingredients = IngredientInlineSerializer(many=True, read_only=True)
    # фото (як URL або null) — теж read-only
    photo = serializers.ImageField(read_only=True)

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
            "ingredients",
            "updated_at",
        ]
        read_only_fields = fields  # весь серіалізатор — тільки читання
