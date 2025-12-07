from django.urls import include, path
from rest_framework.routers import DefaultRouter
from restaurant.views.cart import CartViewSet
from restaurant.views.dishes import CategoryViewSet, DishViewSet, IngredientViewSet
from restaurant.views.orders import OrderViewSet

router = DefaultRouter()
router.register(r"dishes", DishViewSet, basename="dish")
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"ingredients", IngredientViewSet, basename="ingredient")
router.register(r"orders", OrderViewSet, basename="order")
router.register(r"cart", CartViewSet, basename="cart")

urlpatterns = [
    path("", include(router.urls)),
]
