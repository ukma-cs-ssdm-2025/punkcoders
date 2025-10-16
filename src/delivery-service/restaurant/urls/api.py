from django.urls import include, path
from rest_framework.routers import DefaultRouter
from restaurant.views.api.dishes import DishViewSet

router = DefaultRouter()
router.register(r"dishes", DishViewSet, basename="dish")

urlpatterns = [
    path("", include(router.urls)),
]
