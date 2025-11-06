# Звіт про надійність (Лабораторна робота 9)

## 1. Огляд знайдених проблем та їх виправлень

| № | Проблема | Критичність | Патерн надійності | Статус |
| :-- | :--- | :--- | :--- | :--- |
| 1 | Відсутній глобальний таймаут API | **High** | **Timeout** (Таймаут) | ✅ **Виправлено** |
| 2 | Відсутній "Запобіжник" (Error Boundary) | **High** | **Error Boundary** (Запобіжник) / **Fallback UI** | ✅ **Виправлено** |
| 3 | Відсутня валідація на `min` (ціна) | **Medium** | **Guard Clause** (Рання перевірка / Захист) | ✅ **Виправлено** |
| 4 | Ризик "зависання" при оновленні токена | **High** | **Timeout** (Таймаут) | ✅ **Виправлено** |
| 5 | Відсутня обробка помилок завантаження зображень | **Low** | **Fallback** (Запасний варіант) | ⚠️ **Відкрито** |

## 2. Деталі виправлень

### Виправлення 1 і 4: Таймаути в `api.js`

**Проблема:** API-запити могли "зависнути" назавжди, блокуючи UI. Це особливо небезпечно під час оновлення токена.

**Патерн:** **Timeout**. Ми встановили ліміт часу, після якого запит вважається невдалим.

**Код (до):**
```javascript
// api.js
const apiClient = axios.create({
  baseURL: API_URL + VERSION,
});

// ... в interceptor ...
const response = await axios.post(API_URL + 'token/refresh/', {
  refresh: refreshToken
});

**Код (після):**
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
