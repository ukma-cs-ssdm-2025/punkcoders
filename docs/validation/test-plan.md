| № | Компонент / функція | Рівень тесту | Тип (позитивний / негативний) | Очікуваний результат / критерій прийняття |
|---|----------------------|--------------|--------------------------------|--------------------------------------------|
| 1 | Створення страв ([US-001](requirements/user-stories.md#US-001)) | Integration | Негативний | Анонімний користувач не може створити страву |
| 2 | Створення страв ([US-001](requirements/user-stories.md#US-001), [FR-043](requirements/requirements.md#FR-043)) | Integration | Позитивний | Менеджер може створити страву, якщо надасть валідні дані та фото ([FR-043](requirements/requirements.md#FR-043)) |
| 3 | Система авторизації ([PERF-005](requirements/requirements.md#PERF-005)) | System | Позитивний | Користувач вводить валідні дані, заходить у систему й бачить профіль |
| 4 | Система авторизації ([SEC-001](requirements/requirements.md#SEC-001)) | Unit | Позитивний | Паролі у БД захешовані Argon2id згідно з [SEC-001](requirements/requirements.md#SEC-001) |
| 5 | Пермишени для менеджера ([C-001](requirements/requirements.md#C-001)) | Integration | Негативний | Якщо у `permission_classes` потрібен менеджер, доступ користувачу-замовнику дає 403 |
| 6 | Dashboard кухаря ([US-011](requirements/user-stories.md#US-011), [FR-051](requirements/requirements.md#FR-051)) | Integration | Позитивний | Кухар бачить нове замовлення в реальному часі |
| 7 | Dashboard кухаря ([US-011](requirements/user-stories.md#US-011), [FR-051](requirements/requirements.md#FR-051)) | Integration | Негативний | Незалогінений користувач не бачить панель кухні |
| 8 | Dashboard кухаря ([US-011](requirements/user-stories.md#US-011), [FR-051](requirements/requirements.md#FR-051)) | Integration | Негативний | Залогінений не-кухар/не-менеджер не має доступу |
| 9 | Керування меню ([US-001](requirements/user-stories.md#US-001), [FR-043](requirements/requirements.md#FR-043)) | Integration | Негативний | Помилка валідації, якщо немає обов’язкової назви ([FR-043](requirements/requirements.md#FR-043)) — не зберігає |
| 10 | Недоступні страви ([US-001](requirements/user-stories.md#US-001), [FR-048](requirements/requirements.md#FR-048), [FR-050](requirements/requirements.md#FR-050)) | System | Позитивний | Менеджер позначає страву «недоступна» ([FR-048](requirements/requirements.md#FR-048)); користувач не може додати в кошик ([FR-050](requirements/requirements.md#FR-050)) |
| 11 | Оформлення замовлення без акаунта ([US-016](requirements/user-stories.md#US-016), [FR-035](requirements/requirements.md#FR-035)) | System | Позитивний | Гість вводить мінімальні дані та успішно завершує замовлення |
| 12 | Ліміт на кількість страв ([US-014](requirements/user-stories.md#US-014), [FR-055](requirements/requirements.md#FR-055), [FR-056](requirements.md#FR-056)) | Integration | Негативний | При спробі додати 6-ту страву при ліміті 5 — відмова з повідомленням |
| 13 | Порожній кошик ([FR-016](requirements/requirements.md#FR-016)) | Integration | Негативний | Кнопка «Оформити замовлення» неактивна або помилка при порожньому кошику |
| 14 | Зміна статусу замовлення ([FR-022](requirements/requirements.md#FR-022), [FR-023](requirements/requirements.md#FR-023)) | Integration | Позитивний | «Взяти замовлення» переводить статус у «У доставці» |
| 15 | Реальний час на кухні ([US-011](requirements/user-stories.md#US-011), [FR-051](requirements/requirements.md#FR-051)) | Integration | Позитивний | Нове замовлення з’являється на екрані кухаря автоматично |
| 16 | Юзабіліті метрика ([USAB-001](requirements/requirements.md#USAB-001)) | Acceptance | Позитивний (NFR) | 80% нових користувачів оформляють замовлення < 3 хв |

