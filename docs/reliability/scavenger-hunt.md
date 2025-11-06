# Документація помилок та їх усунення

potential leaky error messages - check backend views?

№,Проблема,Код (Фрагмент),Чому небезпечно,Fault → Error → Failure,Severity

1,Відсутній глобальний таймаут API, api.js:const apiClient = axios.create(...),"Якщо бекенд ""зависне"" або буде повільно відповідати, axios чекатиме вічно.","Fault: axios.create не має опції timeout.Error: Мережевий запит знаходиться у стані pending нескінченно довго.Failure: Користувач бачить нескінченний завантажувач (наприклад, при завантаженні категорій), і весь додаток перестає відповідати на запити.",High
 ОСОББЛИВО ВАЖЛИВО: "Ризик ""зависання"" при оновленні токена",api.js (interceptor):await axios.post(...),"Запит на оновлення токена (/token/refresh/) сам по собі не має таймауту. Якщо цей запит зависне, всі майбутні запити зупиняться.","Fault: axios.post для оновлення токена викликається без timeout.Error: Запит на оновлення токена ""зависає"".Failure: Оригінальний запит (який спричинив 401) та всі нові запити блокуються, доки не оновиться токен, що ніколи не станеться.",High

2,"Відсутній ""Запобіжник"" (Error Boundary)",App.jsx:<Routes>...</Routes>,"Якщо будь-який компонент (наприклад, HomePage) ""впаде"" через несподівану помилку рендерингу (наприклад, data.user.name де user є null), весь додаток ""зламається"" (білий екран).",Fault: React-додаток не має компонента ErrorBoundary.Error: Помилка JavaScript спливає до кореня React-дерева.Failure: Користувач бачить білий екран смерті (WSOD) замість запасного UI і не може нічого зробити.,High

3,Відсутня валідація на min (ціна),"AdminMenuManagement.jsx:{...register('price', ...)}",Форма дозволяє користувачу вводити та надсилати від'ємні числа для ціни.,"Fault: Відсутнє правило min: 0 у валідації react-hook-form.Error: Стан форми містить некоректне значення (price: -50).Failure: На бекенд надсилаються невалідні дані, що спричиняє помилку 400 (яку ви, на щастя, обробляєте!), але краще ""зловити"" це на клієнті.",Low

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