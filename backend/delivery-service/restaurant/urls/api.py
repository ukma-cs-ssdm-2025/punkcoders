from django.urls import include, path
from rest_framework.routers import DefaultRouter
from restaurant.views.dishes import CategoryViewSet, DishViewSet, IngredientViewSet

router = DefaultRouter()
router.register(r"dishes", DishViewSet, basename="dish")
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"ingredients", IngredientViewSet, basename="ingredient")

urlpatterns = [
    path("", include(router.urls)),
]
