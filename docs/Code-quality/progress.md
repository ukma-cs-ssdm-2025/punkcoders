# Code Quality Progress — PunkCoders 🍕🚀
---

## 👩🏻‍💻 Backend (Django REST API)

- [x] Створено базову структуру проєкту Django (`delivery-service`)
- [x] Реалізовано CRUD для `DishViewSet` з mock data
- [x] Підключено DRF Spectacular (автогенерація OpenAPI)
- [x] Реалізовано тести API (`test_dishes_api.py`)
- [x] Валідація input → перевірка некоректних даних (400)
- [ ] Перевірка статус-кодів (200, 201, 204, 400, 404)
- [x] Перехід на ORM (створення моделей, міграції, реальні дані)
- [x] Підключити базу даних PostgreSQL через Docker
- [ ] Додати покриття тестами для фільтрації та сортування

---

## 🧩 API Documentation

- [x] Автоматично генерується OpenAPI (`/api/v0/schema/`)
- [x] Swagger UI доступний на `/api/v0/docs/`
- [ ] Оновити описи у YAML (додати фільтрацію, сортування)
- [ ] Додати приклади запитів/відповідей (Swagger examples)
- [ ] Перевірити відповідність OpenAPI ↔ тестам

---

## 🧪 Testing

- [x] Налаштовано базові `APITestCase`
- [x] Тести на валідацію input
- [x] Тести на статус-коди (200, 201, 404)
- [ ] Тести на оновлення (`PUT /dishes/{id}/`)
- [ ] Тести на видалення (`DELETE /dishes/{id}/`)

---

## ⚙️ CI/CD & Quality Tools

- [x] Docker працює локально (`app`, `db`)
- [ ] Налаштувати GitHub Actions для автозапуску тестів
- [ ] Додати pre-commit hooks (flake8, black)
- [ ] Запровадити лінтер Python (`flake8`, `black`, `isort`)
- [ ] Додати перевірку тестів у CI/CD pipeline
- [ ] Запуск автогенерації документації при push

---
