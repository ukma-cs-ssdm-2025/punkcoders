from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from restaurant.models import Dish


class Order(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "New"
        PREPARING = "preparing", "Preparing"
        DELIVERING = "delivering", "Delivering"
        COMPLETED = "completed", "Completed"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )

    guest_name = models.CharField(max_length=255, blank=True)
    guest_phone = models.CharField(max_length=50, blank=True)
    guest_address = models.CharField(max_length=500, blank=True)

    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        if self.user:
            return f"Order #{self.id} — {self.get_status_display()} — User {self.user.email}"
        return f"Order #{self.id} — {self.get_status_display()} — Guest {self.guest_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    dish = models.ForeignKey(Dish, on_delete=models.PROTECT, related_name="order_items")
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))])

    class Meta:
        unique_together = ("order", "dish")

    def __str__(self):
        return f"{self.dish.name} x{self.quantity}"
