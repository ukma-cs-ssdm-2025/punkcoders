from django.db import transaction
from restaurant.models import Dish, DishIngredient

# NOTE: The dish_to_dict function has been removed as it is no longer needed.
# The serializers now handle all conversion from model instance to JSON.


def get_dishes_queryset(category_id=None):
    """
    Returns a queryset of available dishes, optionally filtered by category_id.
    """
    # Start with all available dishes and pre-load related data
    # to prevent N+1 query problems.
    queryset = Dish.objects.select_related("category").prefetch_related(  # .filter(is_available=True)
        "dishingredient_set__ingredient"
    )

    # If a category_id is provided, filter the queryset
    if category_id:
        # Use category_id=category_id for a direct foreign key check
        queryset = queryset.filter(category_id=category_id)

    # Order by name by default
    queryset = queryset.order_by("name")

    return queryset


@transaction.atomic
def create_dish(validated_data):
    """
    Creates a new dish from serializer's validated_data.
    This service no longer needs to worry about validating IDs, the serializer does it.
    """
    # The 'ingredients_data' is not a model field, so we pop it.
    ingredients_data = validated_data.pop("ingredients_data", [])

    # The serializer's 'category_id' field provides the 'category' instance directly.
    dish = Dish.objects.create(**validated_data)

    if ingredients_data:
        # Simplified ingredient handling
        dish_ingredients = [
            DishIngredient(
                dish=dish, ingredient_id=item["ingredient_id"], is_base_ingredient=item.get("is_base_ingredient", True)
            )
            for item in ingredients_data
        ]
        DishIngredient.objects.bulk_create(dish_ingredients)

    return dish


@transaction.atomic
def update_dish(dish_instance, validated_data):
    """
    Updates an existing dish instance from serializer's validated_data.
    """
    ingredients_data = validated_data.pop("ingredients_data", None)

    # Update basic fields
    for attr, value in validated_data.items():
        setattr(dish_instance, attr, value)

    dish_instance.save()

    # If ingredients_data is provided, replace existing ingredients
    if ingredients_data is not None:
        DishIngredient.objects.filter(dish=dish_instance).delete()
        dish_ingredients = [
            DishIngredient(
                dish=dish_instance,
                ingredient_id=item["ingredient_id"],
                is_base_ingredient=item.get("is_base_ingredient", True),
            )
            for item in ingredients_data
        ]
        DishIngredient.objects.bulk_create(dish_ingredients)

    return dish_instance
