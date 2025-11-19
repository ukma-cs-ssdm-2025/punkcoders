from django.urls import include, path
from orders.views.orders import OrderViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"", OrderViewSet, basename="order")

urlpatterns = [
    path("", include(router.urls)),
]
