# Фінальний звіт

Результатом наших страждань є barebones сайт оналйн-доставки для якого-небудь ресторану. Він дозволяє працівникам керувати меню і слідкувати за замовленнями, а користувачам - замовляти їжу без смс та реєстрації.

## Виконання вимог

Виконано майже всі must-have і майже ніяких good-to-have. Чекліст для must-have (жирних):

Виконані: [US-001](../docs/requirements/user-stories.md#us-001), [US-006](../docs/requirements/user-stories.md#us-006), [US-008](../docs/requirements/user-stories.md#us-008), [US-011](../docs/requirements/user-stories.md#us-011), [US-012](../docs/requirements/user-stories.md#us-012), [US-016](../docs/requirements/user-stories.md#us-016), [FR-002](../docs/requirements/requirements.md#fr-002), [FR-011](../docs/requirements/requirements.md#fr-011), [FR-012](../docs/requirements/requirements.md#fr-012), [FR-013](../docs/requirements/requirements.md#fr-013), [FR-014](../docs/requirements/requirements.md#fr-014), [FR-016](../docs/requirements/requirements.md#fr-016), [FR-017](../docs/requirements/requirements.md#fr-017), [FR-018](../docs/requirements/requirements.md#fr-018), [FR-005](../docs/requirements/requirements.md#fr-005), [FR-022](../docs/requirements/requirements.md#fr-022), [FR-052](../docs/requirements/requirements.md#fr-052), [FR-023](../docs/requirements/requirements.md#fr-023), [FR-024](../docs/requirements/requirements.md#fr-024), [FR-025](../docs/requirements/requirements.md#fr-025), [FR-026](../docs/requirements/requirements.md#fr-026), [FR-031](../docs/requirements/requirements.md#fr-031), [FR-034](../docs/requirements/requirements.md#fr-034) (good-to-have), [FR-035](../docs/requirements/requirements.md#fr-035), [FR-043](../docs/requirements/requirements.md#fr-043), [FR-044](../docs/requirements/requirements.md#fr-044), [FR-046](../docs/requirements/requirements.md#fr-046), [FR-048](../docs/requirements/requirements.md#fr-048), [FR-050](../docs/requirements/requirements.md#fr-050), [SEC-001](../docs/requirements/requirements.md#sec-001)

Частково виконані: [FR-022](../docs/requirements/requirements.md#fr-022) (2), [FR-049](../docs/requirements/requirements.md#fr-049) (4)

Не виконані: [US-014](../docs/requirements/user-stories.md#us-014) & [FR-055](../docs/requirements/requirements.md#fr-055) & [FR-056](../docs/requirements/requirements.md#fr-056) (5), [FR-057](../docs/requirements/requirements.md#fr-057) & [FR-059](../docs/requirements/requirements.md#fr-059) (5), [FR-001](../docs/requirements/requirements.md#fr-001) (1), [FR-032](../docs/requirements/requirements.md#fr-032) & [FR-033](../docs/requirements/requirements.md#fr-033) (3)

Не протестовані: [SEC-002](../docs/requirements/requirements.md#sec-002), [SEC-003](../docs/requirements/requirements.md#sec-003), [PERF-001](../docs/requirements/requirements.md#perf-001), [PERF-003](../docs/requirements/requirements.md#perf-003), [PERF-005](../docs/requirements/requirements.md#perf-005), [PERF-006](../docs/requirements/requirements.md#perf-006), [USAB-001](../docs/requirements/requirements.md#usab-001), [USAB-003](../docs/requirements/requirements.md#usab-003), [USAB-004](../docs/requirements/requirements.md#usab-004)

(1) фіг з нею, чесно, one click away, Дора старалась
(2) в станах замовлення вийшов трохи срач, але він тільки внутрішній, тому то таке
(3) немає можливості вказати готівка чи кредитка в системі, але кур'єр все одно фізично може прийняти готівку або дати термінал
(4) не в кінці всього списку і не дуже сірими
(5) не реалізована система налаштувань сайту

## Опис роботи

При першому запуску програми автоматично створюється акаунт менеджера з кредами, вказаними в .env. Після цьго цей менеджер може додавати нових працівників (менеджерів, кухарів, кур'єрів, касирів), змінювати ролі наявним парцівникам (крім самого себе) та видаляти працівників (деактивувати, якщо на них підв'язаний якийсь запис в БД). Кожен працівник має сторінку профіля, де він може змінити свої особисті дані (не роль) і пароль. Можливі паролі обмежені рейтингом zxcvbn - не менше 3/4.

Менеджер також може додавати/редагувати/видаляти категорії та страви. Страви мають мати назву, опис, категорію та ціну, можуть бути позначені як недоступні (тоді їх не можна замовити), і можуть мати або не мати фото. Будь-який користувач, авторизований чи ні, може переглянути меню (з вкладками для кожної категорії), покласти доступні страви до кошика та оформити замовлення, вказавши номер телефона та адресу чи самовивіз. Далі замовлення з'являється на екрані кухаря, який може взяти його в роботу,  апотім помітити як готове. Після цього воно приходить кур'єру, який може взяти його до доставки і потім помітити як доставлене/сплачене. А якщо це замовлення на самовивіз, воно приходить касиру, який може відмітити його як віддане людині (та оплачене).

Цей функціонал технічно достатній для користування системи, але ми хотіли, хоч насправді і не могли, зробити набагато більше. Сайт мав би підтримувати акаунти для клієнтів для участі в програмі лояльності, онлайн-оплату, сторінку FAQ, налаштовуване обмеження на кількість страв яку можна замовити, сортування та фільтрацію меню за інгредієнтами, прохання змінити страву (без цибулі, будь ласка) та інше. Але чого ми могли досягти кращим робочим процесом це адекватнішої архітектури, чистішого та надійнішого коду і меншої кількості багів.
