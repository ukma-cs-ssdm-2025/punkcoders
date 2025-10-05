# Traceability-matryx

| Requirement ID                                 | Requirement Description                                 | Components / Modules                                                                                           |
| ---------------------------------------------- | ------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| FR-001, FR-002, FR-003, FR-004, FR-005, FR-008 | Перегляд меню, категорії, сортування, фільтрація, пошук | **Web UI**, **Backend (Menu Service)**, **DB**                                                                 |
| FR-006, FR-007                                 | Улюблені страви                                         | **Web UI**, **Backend (User Service)**, **DB**                                                                 |
| FR-009, FR-010                                 | Кастомна піца                                           | **Web UI**, **Backend (Order/Menu Service)**, **DB**                                                           |
| FR-011 – FR-021                                | Кошик і оформлення замовлення                           | **Web UI**, **Backend (Order Service)**, **DB**                                                                |
| FR-022 – FR-026                                | Доставка (статуси, кур’єр, мапа)                        | **Web UI (Courier Panel)**, **Backend (Order Service)**, **Mapbox Integration**, **DB**                        |
| FR-027 – FR-033                                | Оплата (готівка, картка, LiqPay)                        | **Web UI**, **Backend (Payment Service)**, **LiqPay**                                                          |
| FR-034 – FR-042                                | UX + акаунти, логін/реєстрація                          | **Web UI**, **Backend (Auth & User Service)**, **DB**                                                          |
| FR-043 – FR-050                                | Керування меню менеджером                               | **Web UI (Manager Panel)**, **Backend (Menu Service)**, **DB**                                                 |
| FR-051 – FR-056                                | Робота персоналу (кухар, кур’єр, менеджер)              | **Web UI (Staff Panels)**, **Backend (Order/Report Services)**, **Mapbox**, **DB**                             |
| FR-057 – FR-059                                | FAQ та техпідтримка                                     | **Web UI**, **Backend (Support Service)**, **DB**                                                              |
| PERF-001 – PERF-006                            | Час відгуку UI та бекенду                               | **Web UI (оптимізація SPA/MPA)**, **Backend (Django performance tuning)**, **DB indexing**, **Load balancing** |
| SEC-001 – SEC-005                              | Безпека (паролі, TLS, оплати)                           | **Backend (Auth Service, Payment Service)**, **LiqPay**, **HTTPS/TLS stack**                                   |
| REL-001 – REL-002                              | Надійність (uptime, збереження кошика)                  | **Backend (fault tolerance)**, **DB replication**, **Frontend (local storage)**                                |

# 2. Quality Attribute Scenarios

### Performance Scenario
- **Stimulus**: 100 користувачів одночасно відкривають сторінку меню.
- **Environment**: production-сервер, нормальне навантаження (до 100 одночасних користувачів).
- **Response**: система відображає меню без помилок.
- **Response Measure**: 95% запитів виконуються < **1 секунди** (NFR PERF-001).
### Reliability Scenario
- **Stimulus**: користувач додає страви у кошик і втрачає інтернет-з’єднання.
- **Environment**: клієнтський браузер, нестабільна мережа.
- **Response**: кошик зберігається локально у браузері. Після відновлення мережі синхронізується з бекендом.
- **Response Measure**: жодна страва не втрачається, час відновлення < **3 секунд** після перепідключення (NFR REL-002).
