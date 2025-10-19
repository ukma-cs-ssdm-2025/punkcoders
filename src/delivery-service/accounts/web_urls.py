from django.urls import path

from . import web_views

app_name = "accounts"

urlpatterns = [
    path("register/", web_views.register_view, name="register"),
    path("login/", web_views.login_view, name="login"),
    path("logout/", web_views.logout_view, name="logout"),
    # We'll add a dummy manager page here for testing
    # path('dashboard/', web_views.manager_dashboard_view, name='manager_dashboard'),
]
