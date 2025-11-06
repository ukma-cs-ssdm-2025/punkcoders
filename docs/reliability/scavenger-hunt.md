# Звіт про надійність (Лабораторна робота 9)

## 1. Огляд знайдених проблем та їх виправлень

| № | Проблема | Критичність | Патерн надійності | Статус |
| :-- | :--- | :--- | :--- | :--- |
| 1 | Відсутній глобальний таймаут API | **High** | **Timeout** (Таймаут) | ✅ **Виправлено** |
| 2 | Відсутній "Запобіжник" (Error Boundary) | **High** | **Error Boundary** (Запобіжник) / **Fallback UI** | ⚠️ **Відкрито** |
| 3 | Відсутня валідація на `min` (ціна) | **Medium** | **Guard Clause** (Рання перевірка / Захист) | ⚠️ **Відкрито** |
| 4 | Ризик "зависання" при оновленні токена | **High** | **Timeout** (Таймаут) |  ⚠️ **Відкрито** |
| 5 | Відсутня обробка помилок завантаження зображень | **Low** | **Fallback** (Запасний варіант) | ⚠️ **Відкрито** |

## 2. Деталі виправлень

### Виправлення 1 і 4: Таймаути в `api.js`

**Проблема:** API-запити могли "зависнути" назавжди, блокуючи UI. Це особливо небезпечно під час оновлення токена.

**Патерн:** **Timeout**. Ми встановили ліміт часу, після якого запит вважається невдалим.

**Код (до):**
```
javascript
// api.js
const apiClient = axios.create({
  baseURL: API_URL + VERSION,
});

// ... в interceptor ...
const response = await axios.post(API_URL + 'token/refresh/', {
  refresh: refreshToken
});
```

**Код (після):**
```
const apiClient = axios.create({
  baseURL: API_URL + VERSION,
  timeout: 10000, // 10 секунд
});

// ... в interceptor ...
const response = await axios.post(API_URL + 'token/refresh/', {
  refresh: refreshToken
}, {
  timeout: 5000 // 5 секунд
});
```


potential leaky error messages - check backend views?


warn the user that deleting a category will delete its dishes, OR BETTER, USE PROTECT/NO ACTION

Переконатись, що якщо ці місця можуть отримати 404, вони обробляються окремо:
AdminCategoryManagement.jsx:

- onSubmit (when editing)
- handleDelete

AdminMenuManagement.jsx:

- onSubmit (when editing)
- handleDelete
- handleAvailabilityToggle

MenuPage.jsx:

- fetchDishesByCategory

- fetchDishDetails


В файлі create_initial_manager.py:
  A. Обробка помилок занадто широке перехоплення (except Exception): 
  ```
  except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error creating manager: {e}"))
  ```
| Поле         | Значення                                                        |
| ------------ | --------------------------------------------------------------- |
| **Fault**    | Надто широке виключення `except Exception`                      |
| **Error**    | Реальна причина помилки прихована                               |
| **Failure**  | Адмін бачить лише загальне повідомлення, проблема не усувається |
| **Severity** | Medium                                                          |
**Як виправити: перехоплювати тільки очікувані помилки**

В файлі backend\delivery-service\restaurant\serializers\dishes.py:
  C. Валідація вхідних даних:
  ingredients_data не перевіряє існування інгредієнтів:
  ```
  class IngredientDataSerializer(serializers.Serializer):
    ingredient_id = serializers.IntegerField()
    is_base_ingredient = serializers.BooleanField(default=True)

  ```
| Поле         | Значення                                                          |
| ------------ | ----------------------------------------------------------------- |
| Fault        | Немає перевірки існування Ingredient перед використанням          |
| Error        | У `validated_data` з’являється посилання на неіснуючий інгредієнт |
| Failure      | Страва не створюється або створюється з некоректними зв’язками    |
| **Severity** | **High**                                                          |
**Як виправити: додати валідацію**

В файлі backend\delivery-service\restaurant\services\dishes.py:
D. Потенційні "silent failures":
update_dish видаляє всі інгредієнти навіть якщо частина невалідна:
```
def update_dish(dish_instance, validated_data):
    """
    Updates an existing dish instance from serializer's validated_data.
    """
    ingredients_data = validated_data.pop("ingredients_data", None)

    # Update basic fields
    for attr, value in validated_data.items():
        setattr(dish_instance, attr, value)

    dish_instance.save()

    # If ingredients_data is provided, replace existing ingredients
    if ingredients_data is not None:
        DishIngredient.objects.filter(dish=dish_instance).delete()
        dish_ingredients = [
            DishIngredient(
                dish=dish_instance,
                ingredient_id=item["ingredient_id"],
                is_base_ingredient=item.get("is_base_ingredient", True),
            )
            for item in ingredients_data
        ]
        DishIngredient.objects.bulk_create(dish_ingredients)

    return dish_instance
```
| Поле         | Значення                                         |
| ------------ | ------------------------------------------------ |
| **Fault**    | Операція replace не має rollback на рівні логіки |
| **Error**    | Дані dish тимчасово в неповному стані            |
| **Failure**  | Dish може залишитися без інгредієнтів            |
| **Severity** | High                                             |



