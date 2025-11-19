import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from restaurant.models import Category, Dish

User = get_user_model()


@pytest.mark.django_db
def test_create_order_success():
    client = APIClient()

    # Створюємо юзера
    user = User.objects.create_user(
        email="test@example.com",
        password="Test12345!",
        first_name="Test",
        last_name="User",
        role=User.Role.MANAGER,
    )

    # Логінимось → отримуємо токен
    response = client.post("/api/token/", {"email": "test@example.com", "password": "Test12345!"})

    access_token = response.data["access"]
    client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)

    # Створюємо тестову страву
    cat = Category.objects.create(name="Pizza")
    dish = Dish.objects.create(
        name="Margherita",
        category=cat,
        price=100,
        description="Test pizza",
        is_available=True,
    )

    response = client.post(
        "/api/v0/orders/",
        {
            "dishes": [dish.id],
        },
        format="json",
    )

    assert response.status_code == 201
    assert response.data["user_id"] == user.id
    assert response.data["total_price"] == "100.00"
