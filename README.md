# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) (or [oxc](https://oxc.rs) when used in [rolldown-vite](https://vite.dev/guide/rolldown)) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.
# Punkcoders - Food Delivery App

![CI Status](https://github.com/ukma-cs-ssdm-2025/team-team12/actions/workflows/ci.yml/badge.svg)

## Team Info

- Олешко Дар'я (Doodlinka, d.oleshko@ukma.edu.ua) - Repo Maintainer, Quality Lead
- Омельченко Дар'я (dar11ya, d.omelchenko@ukma.edu.ua) - Documentation Lead, Documentation Lead
- Романчук Анна (AnnaRomanchuk, a.romanchuk@ukma.edu.ua) - Issue Tracker Lead, Requirements Lead
- Узун Дмитро (uzun-dmytro, d.uzun@ukma.edu.ua) - CI Maintainer, Traceability Lead
  
## Project Info

Тема №8 - Застосунок координації доставки їжі

- Клієнти замовляють страви, кур'єри доставляють, ресторани керують меню.
- Вимагає врахування продуктивності (оновлення в реальному часі).

## How to run

- Clone the repo
- Install Docker
- If you don't have src/.env, copy src/.env.sample into it
- If you don't have src/delivery-service/app/settings.py, copy src/delivery-service/app/settings.py.sample into it
- Run ```cd src && docker-compose up --build```. If it doesn't work, launch the Docker app to ensure the Docker Engine is running, then try again.
- This should run automatically when the app container goes live, but if it doesn't, run ```docker exec -it src-app-1 python manage.py migrate```
- Go to localhost:8000 in your browser

## СТРАТЕГІЯ ГІЛКУВАННЯ

- На main лише версії проєкту, в яких все, що реалізовано, реалізовано повністю та без проблем. Заливаємо ЛИШЕ через PR і ЛИШЕ з dev. Будь-яку версію на main не соромно показати, і великі досягнення будуть протеговані як релізи. Всі PR потребують, щоб мінімум одна ішна людина підтвердила, що це достойно проду.
- На dev версії, які ще не готові, але вже не катастрофічно зламані. Звідси ми робимо міні-гілки і тут збираємо і відлагоджуємо зміни перед тим, як відправити на main. Сюди робимо PR з тимчасових гілок. Підтверджувати PR іншій людині не необхідно. (Технічно можна, але не рекомендовано, пушити сюди без PR, але ТІЛЬКИ для невеликих змін, будь ласка.)
- Для кожної значної зміни - створити фічу, виправити баг тощо - ми створюємо тимчасову гілку, на якій працюємо. Коли закіничли роботу, робимо PR на dev і видаляємо гілку після злиття. Це для того, щоб не плутатись один у одного під ногами і розуміти, який коміт над чим працює і де щось зламалось. Гілки називаємо як тип/зміна, можна тип/зміна-номер-issue, щоб розуміти нащо гілка існує. Наприклад, feature/user-authentication, bugfix/null-pointer-when-saving, experiment/new-algo-eval.

## Управління артефактами

- Усі документи з вимогами зберігаються в репозиторії у каталозі: /docs/requirements/
- README.md містить актуальні посилання на ключові документи та артефакти.

## TODO впровадження стратегії гілкування

- Для PR у main та dev поки не налаштовано, які перевірки треба проходити, бо перевірок ще немає.
- Вирішити, чи вимкнути "Require branches to be up to date before merging" - сповільнює процес, але запобігає ситуації, коли А працює, Б працює, але А+Б крашиться. Напевно, вимкнемо якщо біситиме.
- Можливо, треба буде перебалансувати необхідну кількість approve для dev та main.

