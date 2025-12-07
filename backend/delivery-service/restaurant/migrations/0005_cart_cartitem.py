import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("restaurant", "0004_order_orderitem"),
    ]

    operations = [
        migrations.CreateModel(
            name="Cart",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("session_key", models.CharField(max_length=40, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Cart",
                "verbose_name_plural": "Carts",
            },
        ),
        migrations.CreateModel(
            name="CartItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200, verbose_name="Dish name snapshot")),
                (
                    "unit_price",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)]
                    ),
                ),
                (
                    "quantity",
                    models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)]),
                ),
                (
                    "line_total",
                    models.DecimalField(
                        decimal_places=2, max_digits=12, validators=[django.core.validators.MinValueValidator(0)]
                    ),
                ),
                (
                    "cart",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="items", to="restaurant.cart"
                    ),
                ),
                (
                    "dish",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, related_name="+", to="restaurant.dish"
                    ),
                ),
            ],
            options={
                "verbose_name": "Cart item",
                "verbose_name_plural": "Cart items",
            },
        ),
        migrations.AlterUniqueTogether(
            name="cartitem",
            unique_together={("cart", "dish")},
        ),
    ]
