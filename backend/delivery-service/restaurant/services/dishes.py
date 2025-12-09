from restaurant.models import Dish


def get_dishes_queryset(category_id=None):
    """
    Returns a queryset of available dishes, optionally filtered by category_id.
    """
    # Start with all available dishes and pre-load related data
    # to prevent N+1 query problems.
    queryset = Dish.objects.select_related("category")

    # If a category_id is provided, filter the queryset
    if category_id is not None:
        # Use category_id=category_id for a direct foreign key check
        queryset = queryset.filter(category_id=category_id)

    # Order by name by default
    queryset = queryset.order_by("name")
    return queryset
