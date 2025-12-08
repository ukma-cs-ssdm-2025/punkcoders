from django.urls import include, path
from rest_framework.routers import DefaultRouter
from restaurant.views.cashier import CashierOrderViewSet
from restaurant.views.courier import CourierOrderViewSet
from restaurant.views.dishes import CategoryViewSet, DishViewSet
from restaurant.views.kitchen import KitchenOrderViewSet
from restaurant.views.orders import OrderViewSet

router = DefaultRouter()
router.register(r"dishes", DishViewSet, basename="dish")
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"orders", OrderViewSet, basename="order")
router.register(r"kitchen/orders", KitchenOrderViewSet, basename="kitchen-order")
router.register(r"courier", CourierOrderViewSet, basename="courier")
router.register(r"cashier/orders", CashierOrderViewSet, basename="cashier-orders")

urlpatterns = [
    path("", include(router.urls)),
]
