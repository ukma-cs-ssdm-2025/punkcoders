from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, transaction
from restaurant.models import Category, Dish, DishIngredient, Ingredient


# ----------------------------------------------------------------------
# Допоміжна функція для перетворення об'єкта Dish на словник
# ----------------------------------------------------------------------
def dish_to_dict(dish_instance):
    """Конвертує об'єкт Dish та його властивості у словник для API."""
    if not dish_instance:
        return None

    return {
        "id": dish_instance.pk,
        "name": dish_instance.name,
        "price": float(dish_instance.price),
        "category": dish_instance.category.name,
        "category_slug": dish_instance.category.slug,
        "description": dish_instance.description,
        "photo_url": dish_instance.photo.url if dish_instance.photo else None,
        "is_available": dish_instance.is_available,
        "ingredients": [
            {"name": di.ingredient.name, "is_base": di.is_base_ingredient}
            for di in dish_instance.dishingredient_set.select_related("ingredient").all()
        ],
    }


# ----------------------------------------------------------------------
# Бізнес-логіка: Отримання страв з фільтрами та сортуванням (FR-001, FR-002, FR-003, FR-004, FR-008)
# ----------------------------------------------------------------------
def get_dishes(category_slug=None, has_ingredients=None, lacks_ingredients=None, search_term=None, sort_by="name"):
    """
    Повертає список страв з можливістю фільтрації та сортування.
    """
    # Початковий QuerySet
    queryset = Dish.objects.select_related("category").prefetch_related("dishingredient_set__ingredient")

    # 1. Фільтрація за доступністю (FR-050)
    queryset = queryset.filter(is_available=True)

    # 2. Фільтрація за категорією (FR-002)
    if category_slug:
        queryset = queryset.filter(category__slug=category_slug)

    # 3. Пошук за назвою (FR-008)
    if search_term:
        queryset = queryset.filter(name__icontains=search_term)

    # 4. Фільтрація за інгредієнтами (FR-004)
    # Інгредієнти, які мають бути (has_ingredients)
    if has_ingredients:
        # Очікуємо список ID інгредієнтів
        for ingredient_id in has_ingredients:
            queryset = queryset.filter(ingredients__pk=ingredient_id)

    # Інгредієнти, яких не має бути (lacks_ingredients)
    if lacks_ingredients:
        # Використовуємо exclude() для виключення страв, що містять небажані інгредієнти
        queryset = queryset.exclude(ingredients__pk__in=lacks_ingredients)

    # 5. Сортування (FR-003)
    if sort_by == "price_asc":
        queryset = queryset.order_by("price")
    elif sort_by == "price_desc":
        queryset = queryset.order_by("-price")
    else:  # За замовчуванням сортуємо за доступністю (недоступні в кінці) і назвою (FR-049)
        # Note: FR-050 вже відфільтровує недоступні, але ми залишаємо сортування name.
        queryset = queryset.order_by("name")

    # Конвертуємо QuerySet у список словників
    return [dish_to_dict(dish) for dish in queryset]


# ----------------------------------------------------------------------
# Бізнес-логіка: Перевірка існування страви
# ----------------------------------------------------------------------
def has_dish(pk):
    """Перевіряє, чи існує страва за її первинним ключем (ID)."""
    try:
        return Dish.objects.filter(pk=pk).exists()
    except (ValueError, TypeError):
        return False


# ----------------------------------------------------------------------
# Бізнес-логіка: Отримання страви за ID
# ----------------------------------------------------------------------
def get_dish_by_id(pk):
    """Повертає одну страву у форматі словника або None, якщо не знайдено."""
    try:
        dish = Dish.objects.get(pk=pk)
        return dish_to_dict(dish)
    except ObjectDoesNotExist:
        return None


# ----------------------------------------------------------------------
# Бізнес-логіка: Створення нової страви (FR-043)
# ----------------------------------------------------------------------
@transaction.atomic
def create_dish(data):
    """
    Створює нову страву, включаючи зв'язки з інгредієнтами.
    Data повинна містити: 'category_id', 'name', 'price', 'description',
    'photo' (файл/url), та опціонально 'ingredients_data'.
    """
    # 1. Валідація та отримання FK-об'єктів
    try:
        category = Category.objects.get(pk=data["category_id"])
    except Category.DoesNotExist:
        raise ValueError("Вказана категорія не знайдена.")
    except KeyError:
        raise ValueError("Відсутнє обов'язкове поле 'category_id'.")

    # 2. Створення об'єкта Dish
    try:
        dish = Dish.objects.create(
            category=category,
            name=data["name"],
            description=data.get("description", ""),
            price=data["price"],
            is_available=data.get("is_available", True),
            # FR-043: Обробка фото. Припускаємо, що 'photo' містить об'єкт файлу.
            photo=data.get("photo"),
        )
    except IntegrityError:
        raise ValueError("Страва з такою назвою вже існує.")
    except KeyError as e:
        raise ValueError(f"Відсутнє обов'язкове поле: {e}")

    # 3. Створення зв'язків DishIngredient
    ingredients_data = data.get("ingredients_data", [])

    if ingredients_data:
        ingredient_ids = [item["ingredient_id"] for item in ingredients_data]
        # Отримуємо всі інгредієнти одним запитом
        ingredients_map = {ing.pk: ing for ing in Ingredient.objects.filter(pk__in=ingredient_ids)}

        if len(ingredients_map) != len(ingredient_ids):
            # Валідація: перевіряємо, чи всі ID інгредієнтів валідні
            invalid_ids = [id for id in ingredient_ids if id not in ingredients_map]
            raise ValueError(f"Знайдено недійсні ID інгредієнтів: {invalid_ids}")

        # Створення зв'язків
        dish_ingredients = []
        for item in ingredients_data:
            ingredient = ingredients_map[item["ingredient_id"]]
            dish_ingredients.append(
                DishIngredient(
                    dish=dish,
                    ingredient=ingredient,
                    # Тепер можна явно задати is_base_ingredient (FR-010)
                    is_base_ingredient=item.get("is_base_ingredient", True),
                )
            )
        DishIngredient.objects.bulk_create(dish_ingredients)

    return dish_to_dict(dish)


# ----------------------------------------------------------------------
# Бізнес-логіка: Оновлення існуючої страви (FR-044) - PATCH-поведінка
# ----------------------------------------------------------------------
@transaction.atomic
def _update_basic_fields(dish, data):
    """Оновлює основні поля страви та повертає, чи були зміни."""
    changed = False
    for field in ["name", "price", "description", "is_available", "photo"]:
        if field in data:
            setattr(dish, field, data[field])
            changed = True
    return changed


def _update_category(dish, data):
    """Оновлює категорію страви та повертає, чи були зміни."""
    if "category_id" in data:
        try:
            # Припускаємо, що Category імпортовано
            category = Category.objects.get(pk=data["category_id"])
            dish.category = category
            return True
        except Category.DoesNotExist:
            raise ValueError("Вказана категорія не знайдена.")
    return False


def _update_ingredients(dish, ingredients_data):
    """
    Оновлює M2M зв'язки інгредієнтів.
    Припускає, що Ingredient і DishIngredient імпортовано.
    """
    if not ingredients_data:
        # Можна обробити як очищення, або пропустити, залежно від вимог
        return

    # 2.1. Валідація всіх інгредієнтів
    ingredient_ids = [item["ingredient_id"] for item in ingredients_data]
    ingredients_map = {ing.pk: ing for ing in Ingredient.objects.filter(pk__in=ingredient_ids)}
    if len(ingredients_map) != len(ingredient_ids):
        raise ValueError("Знайдено недійсні ID інгредієнтів при оновленні.")

    # 2.2. Очищення старих зв'язків
    DishIngredient.objects.filter(dish=dish).delete()

    # 2.3. Створення нових зв'язків
    dish_ingredients = [
        DishIngredient(
            dish=dish,
            ingredient=ingredients_map[item["ingredient_id"]],
            is_base_ingredient=item.get("is_base_ingredient", True),
        )
        for item in ingredients_data
    ]
    DishIngredient.objects.bulk_create(dish_ingredients)


def update_dish(pk, data):
    """
    Оновлює існуючу страву за ID (PATCH-поведінка).
    Включає логіку оновлення інгредієнтів.
    """
    try:
        # Припускаємо, що Dish імпортовано
        dish = Dish.objects.get(pk=pk)

        # 1. Оновлення основних полів та категорії
        changed_basic = _update_basic_fields(dish, data)
        changed_category = _update_category(dish, data)

        if changed_basic or changed_category:
            dish.save()

        # 2. Складна логіка оновлення M2M зв'язків (Інгредієнти)
        if "ingredients_data" in data:
            _update_ingredients(dish, data["ingredients_data"])

        # FR-045: Логіка сповіщення клієнтів про зміни в кошику/неоплаченому замовленні тут.

        # Припускаємо, що dish_to_dict імпортовано
        return dish_to_dict(dish)

    except Dish.DoesNotExist:  # Використовуйте Dish.DoesNotExist, якщо це Django/OR
        # ObjectDoesNotExist є більш точним, ніж ObjectDoesNotExist з Django
        # Якщо Dish.DoesNotExist недоступний, використовуйте ObjectDoesNotExist
        raise ObjectDoesNotExist(f"Страва з ID {pk} не знайдена.")
    except IntegrityError:  # Припускаємо, що IntegrityError імпортовано
        raise ValueError("Страва з такою назвою вже існує.")


# ----------------------------------------------------------------------
# Бізнес-логіка: Видалення страви (FR-046)
# ----------------------------------------------------------------------
def delete_dish(pk):
    """Видаляє страву за ID. Повертає True, якщо видалення відбулося, False, якщо страва не існувала."""
    try:
        dish = Dish.objects.get(pk=pk)
        # FR-047: Тут має бути логіка сповіщення клієнтів, перш ніж ми видалимо.
        dish.delete()
        return True
    except ObjectDoesNotExist:
        # Видалення неіснуючого ресурсу: повертаємо False. View може трактувати це як 204.
        return False
