from accounts.views import LogoutView, SelfUserView, UserViewSet
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),
    path("me/", SelfUserView.as_view(), name="self-user"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
