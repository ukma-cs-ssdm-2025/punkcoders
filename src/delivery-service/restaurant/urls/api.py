from django.urls import path
from restaurant.views.api.dishes import DishListView

urlpatterns = [
	path('dishes/', DishListView.as_view(), name='dish-list'),
]
