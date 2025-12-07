from decimal import Decimal

from autoslug.fields import AutoSlugField
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models


class Category(models.Model):
    """
    Основні категорії страв (Піца, Салати, Напої).
    Містить прапорець для ідентифікації алкогольних напоїв (FR-005).
    """

    name = models.CharField(max_length=100, unique=True, verbose_name="Назва категорії")
    # TODO: remove (downscoped this)
    is_alcoholic = models.BooleanField(
        default=False,
        verbose_name="Алкогольна категорія",
        help_text="Відзначте, якщо категорія містить алкоголь (важливо для обмежень оплати - FR-020).",
    )
    slug = AutoSlugField(
        populate_from="name",
        unique=True,
        always_update=False,
        max_length=100,
    )

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """
    Доступні інгредієнти, які використовуються в стравах.
    """

    name = models.CharField(max_length=100, unique=True, verbose_name="Назва інгредієнта")
    # is_available can be used later if some ingredients run out.
    is_available = models.BooleanField(default=True, verbose_name="Доступний для використання")

    class Meta:
        verbose_name = "Інгредієнт"
        verbose_name_plural = "Інгредієнти"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Dish(models.Model):
    """
    Основна модель для страв у меню.
    """

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="dishes", verbose_name="Категорія")
    name = models.CharField(max_length=200, unique=True, verbose_name="Назва страви")
    description = models.TextField(verbose_name="Опис", help_text="Короткий опис страви та її складу.")
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)], verbose_name="Ціна")
    photo = models.ImageField(
        upload_to="dishes_photos/",
        null=True,
        blank=True,
        verbose_name="Фото страви",
        help_text="Обов'язкове поле для відображення в меню (FR-043).",
    )
    # FR-048: Менеджер може позначити страву як тимчасово недоступну.
    is_available = models.BooleanField(
        default=True,
        verbose_name="Доступна для замовлення",
        help_text="Якщо вимкнено, страва позначається 'тимчасово недоступна' (UC-001).",
    )

    # M2M relationship through DishIngredient
    ingredients = models.ManyToManyField(
        Ingredient, through="DishIngredient", related_name="dishes", verbose_name="Склад страви"
    )

    # FR-045, FR-047: Поля для відстеження змін, які можуть знадобитися для нотифікацій.
    # TODO: remove (downscoped?)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Страва"
        verbose_name_plural = "Меню страв"
        # FR-049: Сортування, щоб недоступні страви йшли в кінці.
        ordering = ["-is_available", "name"]

    def __str__(self):
        availability = "✅" if self.is_available else "❌"
        return f"{availability} {self.name} ({self.price} грн)"


class DishIngredient(models.Model):
    """
    Проміжна модель для зв'язку "Страва - Інгредієнт".
    Використовується, щоб відрізнити базові інгредієнти від тих, які можна додавати/видаляти.
    """

    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, verbose_name="Страва")
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, verbose_name="Інгредієнт")
    # Позначає, чи є цей інгредієнт частиною стандартного рецепта.
    is_base_ingredient = models.BooleanField(
        default=True,
        verbose_name="Базовий інгредієнт",
        help_text="Якщо це базовий інгредієнт, користувач може його прибрати (FR-015). Якщо ні, користувач може його додати.",
    )

    class Meta:
        unique_together = ("dish", "ingredient")
        verbose_name = "Склад страви"
        verbose_name_plural = "Склад страв"

    def __str__(self):
        type_str = "База" if self.is_base_ingredient else "Опція"
        return f"{self.dish.name} - {self.ingredient.name} ({type_str})"


class Order(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "New"
        IN_PROGRESS = "in_progress", "In progress"
        WAITING_FOR_COURIER = "waiting_for_courier", "Waiting for courier"
        DELIVERING = "delivering", "Delivering"
        PAID_CREDIT = "paid_credit", "Paid (credit)"
        AWAITING_CASH = "awaiting_cash", "Awaiting cash payment"
        PAID_CASH = "paid_cash", "Paid (cash)"

    class PaymentMethod(models.TextChoices):
        CREDIT = "credit", "Credit"
        CASH = "cash", "Cash"

    status = models.CharField(max_length=32, choices=Status.choices, default=Status.NEW)
    payment_method = models.CharField(
        max_length=16,
        choices=PaymentMethod.choices,
        default=PaymentMethod.CASH,
        verbose_name="Payment method",
    )

    # Delivery address: optional if самовивіз True
    delivery_address = models.TextField(null=True, blank=True, verbose_name="Delivery address")
    self_pickup = models.BooleanField(default=False, verbose_name="Самовивіз")

    # Phone: simple validation (ukraine-compatible). Adjust regex if you have other formats.
    phone_regex = RegexValidator(
        regex=r"^\+?\d{7,15}$",
        message="Phone number must be entered in the format: +380501234567 or 0501234567. Up to 15 digits allowed.",
    )
    phone = models.CharField(validators=[phone_regex], max_length=20, verbose_name="Phone number")

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Cached total price (sum of item totals). Kept for quick queries.
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ["-created_at"]

    def clean(self):
        # Ensure either delivery_address is set XOR self_pickup is True (one or the other)
        if self.self_pickup and self.delivery_address:
            raise ValidationError("If self_pickup is True, delivery_address must be empty.")
        if (not self.self_pickup) and (not self.delivery_address):
            raise ValidationError("Either delivery_address must be set or self_pickup must be True.")

    def __str__(self):
        return f"Order #{self.id} — {self.get_status_display()} — {self.total_amount} грн"

    def mark_paid_if_self_pickup(self):
        """
        Business rule from issue:
        - Самовивіз orders go from waiting_for_courier to paid for instantly.
        We'll interpret: if self_pickup==True, then once items are created,
        set status to PAID_CASH or PAID_CREDIT depending on payment_method.
        """
        if self.self_pickup:
            if self.payment_method == self.PaymentMethod.CREDIT:
                self.status = self.Status.PAID_CREDIT
            else:
                # default treat as cash
                self.status = self.Status.PAID_CASH
            self.save(update_fields=["status"])


class OrderItem(models.Model):
    """
    Helper table to store one-to-many items of an order.
    We snapshot unit_price at the time of ordering to preserve history.
    """

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    # store dish reference for traceability; if deletion of dish is allowed, keep on_delete=models.PROTECT or SET_NULL
    dish = models.ForeignKey("Dish", on_delete=models.PROTECT, related_name="+")
    name = models.CharField(max_length=200, verbose_name="Dish name snapshot")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    line_total = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])

    class Meta:
        verbose_name = "Order item"
        verbose_name_plural = "Order items"

    def save(self, *args, **kwargs):
        # ensure line_total is consistent
        self.line_total = (self.unit_price or Decimal("0.00")) * Decimal(self.quantity)
        super().save(*args, **kwargs)
