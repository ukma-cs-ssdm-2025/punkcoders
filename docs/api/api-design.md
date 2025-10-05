# API Design — Food Delivery App

## 1. Мета
API для сервісу доставки їжі. Дозволяє переглядати меню, створювати замовлення, керувати замовленнями та перевіряти їх статус.

## 2. Ресурси
- **Dish (страва)**
  - id (int)
  - name (string)
  - price (float)
  - is_available (boolean)

- **Order (замовлення)**
  - id (int)
  - user_id (int)
  - dishes (list of Dish IDs)
  - total_price (float)
  - status (enum: "new", "preparing", "delivering", "completed")

- **User**
  - id (int)
  - name (string)
  - email (string)

## 3. Основні ендпоінти
1. `GET /api/v0/dishes/` → список доступних страв  
2. `POST /api/v0/orders/` → створення замовлення (користувач + страви)  
3. `GET /api/v0/orders/{id}/` → перегляд конкретного замовлення  
4. `PATCH /api/v0/orders/{id}/` → оновлення статусу замовлення  
5. `GET /api/v0/users/{id}/orders/` → історія замовлень користувача  

## 4. HTTP методи та статуси
- GET → 200 OK  
- POST → 201 Created, 400 Bad Request  
- PATCH → 200 OK, 400/404  
- DELETE (якщо потрібно) → 204 No Content  

## 5. Валідація параметрів
- `name` у Dish → max 100 символів  
- `price` → > 0  
- `is_available` → boolean  
- `user_email` → валідний email  
- `dishes` → список ID, кожен має існувати  

## 6. Приклади
### POST /api/v0/orders/
```json
{
  "user_id": 1,
  "dishes": [2, 3, 5]
}
