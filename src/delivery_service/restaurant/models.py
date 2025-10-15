from django.core.validators import MinValueValidator
from django.db import models


class Category(models.Model):
    """
    Основні категорії страв (Піца, Салати, Напої).
    Містить прапорець для ідентифікації алкогольних напоїв (FR-005).
    """

    name = models.CharField(max_length=100, unique=True, verbose_name="Назва категорії")
    is_alcoholic = models.BooleanField(
        default=False,
        verbose_name="Алкогольна категорія",
        help_text="Відзначте, якщо категорія містить алкоголь (важливо для обмежень оплати - FR-020).",
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        help_text="URL-friendly назва категорії (автоматично генерується).",
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


# TODO: Додати модель FavoriteDish (M:M User-Dish) пізніше, коли буде готова модель User/Customer.
# TODO: Додати модель CustomPizzaTemplate для FR-009/FR-010, якщо кастомна піца має фіксований шаблон.
