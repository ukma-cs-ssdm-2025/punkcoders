# from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction  # , IntegrityError
from restaurant.models import Dish, DishIngredient  # , Ingredient, Category

# NOTE: The dish_to_dict function has been removed as it is no longer needed.
# The serializers now handle all conversion from model instance to JSON.


def get_dishes_queryset(category_slug=None, search_term=None, sort_by="name"):
    """
    Returns a queryset of dishes with filtering and sorting.
    The view will handle serialization.
    """
    queryset = (
        Dish.objects.filter(is_available=True)
        .select_related("category")
        .prefetch_related("dishingredient_set__ingredient")
    )

    if category_slug:
        queryset = queryset.filter(category__slug=category_slug)

    if search_term:
        queryset = queryset.filter(name__icontains=search_term)

    if sort_by == "price_asc":
        queryset = queryset.order_by("price")
    elif sort_by == "price_desc":
        queryset = queryset.order_by("-price")
    else:
        queryset = queryset.order_by("name")

    return queryset


def get_dish_by_id(pk):
    """Returns a single Dish instance or None."""
    try:
        return Dish.objects.get(pk=pk)
    except (Dish.DoesNotExist, ValueError, TypeError):
        return None


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


def delete_dish(pk):
    """Deletes a dish by ID."""
    dish = get_dish_by_id(pk)
    if dish:
        dish.delete()
        return True
    return False
