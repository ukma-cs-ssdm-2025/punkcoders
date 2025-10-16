from django.urls import path
from restaurant.views.web import dishes

# Вказуємо namespace для уникнення конфліктів назв URL
app_name = "restaurant"

urlpatterns = [
    # FR-001: Список страв (домашня сторінка меню)
    path("", dishes.dish_list, name="dish_list"),
    # Деталі страви (pk - первинний ключ, тобто ID страви)
    path("dish/<int:pk>/", dishes.dish_detail, name="dish_detail"),
]
