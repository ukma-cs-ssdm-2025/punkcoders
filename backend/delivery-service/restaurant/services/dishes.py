from django.db import transaction
from rest_framework.exceptions import ValidationError
from restaurant.models import Dish, DishIngredient, Ingredient

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
    if category_id is not None:
        # Use category_id=category_id for a direct foreign key check
        queryset = queryset.filter(category_id=category_id)

    # Order by name by default
    queryset = queryset.order_by("name")

    return queryset


def _validate_ingredients_payload(ingredients_data):
    """Ensure every ingredient id exists and appears only once before writing to the DB."""
    ingredient_ids = []
    seen_ids = set()
    duplicate_ids = set()

    for item in ingredients_data:
        ingredient_id = item["ingredient_id"]
        ingredient_ids.append(ingredient_id)
        if ingredient_id in seen_ids:
            duplicate_ids.add(ingredient_id)
        else:
            seen_ids.add(ingredient_id)

    if duplicate_ids:
        duplicates = ", ".join(str(ingredient_id) for ingredient_id in sorted(duplicate_ids))
        raise ValidationError({"ingredients_data": f"Duplicate ingredient ids: {duplicates}."})

    existing_ids = set(Ingredient.objects.filter(id__in=ingredient_ids).values_list("id", flat=True))
    missing_ids = sorted(set(ingredient_ids) - existing_ids)
    if missing_ids:
        missing = ", ".join(str(ingredient_id) for ingredient_id in missing_ids)
        raise ValidationError({"ingredients_data": f"Unknown ingredient ids: {missing}."})


@transaction.atomic
def create_dish(validated_data):
    """
    Creates a new dish from serializer's validated_data, validating ingredient references.
    """
    # The 'ingredients_data' is not a model field, so we pop it.
    ingredients_data = validated_data.pop("ingredients_data", [])

    # The serializer's 'category_id' field provides the 'category' instance directly.
    dish = Dish.objects.create(**validated_data)

    if ingredients_data:
        # Guard against bad payloads before touching DishIngredient rows.
        _validate_ingredients_payload(ingredients_data)
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
    Updates an existing dish instance from serializer's validated_data, validating ingredient references.
    """
    ingredients_data = validated_data.pop("ingredients_data", None)

    # Update basic fields
    for attr, value in validated_data.items():
        setattr(dish_instance, attr, value)

    dish_instance.save()

    # If ingredients_data is provided, replace existing ingredients
    if ingredients_data is not None:
        # Validate replacements to avoid duplicate or missing ingredient relationships.
        _validate_ingredients_payload(ingredients_data)
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
