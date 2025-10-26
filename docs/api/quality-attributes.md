# API Quality Attributes — Food Delivery System

Цей документ описує, як команда забезпечує якість REST API для сервісу доставки їжі.  
Метою є визначення ключових атрибутів якості, цілей, способів реалізації та способів вимірювання.

---

## Metrics (коротко)

| **Атрибут** | **Метрика / Як перевірити** |
|--------------|------------------------------|
| **Performance (Швидкодія)** | 95% запитів відповідають за <400 мс |
| **Security (Безпека)** | Тести з некоректними даними не викликають падіння API, повертають 4хх |
| **Usability (Зручність)** | Усі ендпоінти видно у Swagger з прикладами |
| **Maintainability (Підтримуваність)** | OpenAPI YAML генерується автоматично з коду |


---

## Performance

**Target:** 95th percentile response time < 400ms  

**Implementation:**
- Використання Django ORM із базовою фільтрацією та індексами (`order_id`, `user_id`).  
- Простий пошук і вибірка з бази даних без складних join-операцій.  
- Оптимізація запитів (через `select_related`, `prefetch_related`).  
- Використання DRF pagination для великих списків.  

**Measurement:**
- Перевірка часу відповіді `/orders/{id}` у dev-середовищі (<400 мс).  
- Django Debug Toolbar — для моніторингу SQL-запитів.

---

## Security

**Target:** Pass one of OWASP API Security Top 10 checks  

**Implementation:**
- Валідація вхідних даних через DRF serializers.  
- Захист від SQL-ін’єкцій завдяки Django ORM.  
- Використання безпечних статус-кодів (400, 401, 403, 422).  

**Measurement:**
- Перевірка OWASP ZAP або Django security audit.  
- Тести: надсилання некоректних даних → API не падає, повертає 400.  

---

## Usability

**Target:** 100% endpoints documented and testable via Swagger  

**Implementation:**
- Використання Swagger UI з прикладами запитів і відповідей у JSON.  
- Повна генерація OpenAPI YAML через drf-spectacular.  
- Опис усіх параметрів, прикладів та кодів відповіді.  
- Зрозуміла структура ендпоінтів (`/orders/`, `/menu/`, `/payments/`).  

**Measurement:**
- Всі ендпоінти видно в Swagger UI.  
- Документація оновлюється автоматично при кожному push у репозиторій.  

---

## Maintainability

**Target:** API documentation always synchronized with code  

**Implementation:**
- Code-First підхід: OpenAPI генерується автоматично з коду.  
- Розділення ендпоінтів по модулях (`orders`, `menu`, `payments`).  
- Стандартизована структура `/src/api/`.  
- CI-процес оновлює `openapi-generated.yaml` при кожному push.  

**Measurement:**
- Перевірка consistency документації у CI.  
- Успішне проходження pytest та OpenAPI validation.  

---

## Trade-offs Analysis

| **Quality** | **Trade-off** | **Impact** | **Mitigation** |
|--------------|---------------|-------------|----------------|
| Security (валідація) | +20–30 мс до часу відповіді | Низький | Оптимізувати валідатори; застосовувати only-needed fields |
| Performance (ORM) | Простота коду, але додаткові SQL-запити | Середній | Використання `select_related` / `prefetch_related` |
| Maintainability (автогенерація OpenAPI) | Потрібен час на налаштування CI | Низький | Автоматичне оновлення YAML після кожного push |
| Usability (Swagger) | Потребує підтримки описів | Низький | CI перевірка покриття документацією |
