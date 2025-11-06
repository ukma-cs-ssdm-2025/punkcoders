# Refactoring Report

##  Overview

Проведено рефакторинг коду проєкту (frontend + backend) з метою усунення Code Smells, зменшення технічного боргу та покращення якості коду.  
Аналіз виконувався у **SonarCloud** на гілках `pre-refactor` та `post-refactor`.

| Metric | Before (pre-refactor) | After (post-refactor) |
|:--|:--|:--|
| Lines of Code | 2999 | 2977 |
| Reliability Rating | E | A |
| Maintainability Rating | A | A |
| Duplicated Lines | 0.6% | 0.0% |
| Technical Debt | 1.05h | 0h |
| Code Smells | 35 | 0 |

**All automated tests passed successfully after refactoring.**

---

## 🔧 Changes Summary

| Commit | Description | Refactoring Pattern(s) Used |
|:--|:--|:--|
| `fix sonarqube backend issues` | Об’єднано дві команди pip install і chmod в одну | **Simplify Method / Merge Sequential Statements** |
| `Change parseFloat to Number.parseFloat` | Заміна глобальної функції на метод з неймспейсу `Number` для уникнення конфліктів | **Replace Magic Function with Explicit Namespace** |
| `fix sonarcube AdminCategoryManagement` | Виправлення умов та використання optional chaining | **Simplify Conditional / Introduce Optional Chaining** |
| `Prefer globalThis over window` | Замінено `window` на `globalThis` для сумісності у Node та браузері | **Replace Platform-Specific API with Cross-Platform API** |
| `Unexpected negated condition.` | Переписано інверсовану умову для покращення читабельності | **Simplify Conditional Expression** |
| `remove TODO comments` | Видалено застарілі коментарі | **Remove Dead Code / Remove Commented Code** |
| `Update style.css` | Оптимізовано стилі, об’єднано дублікати, зменшено кількість рядків | **Consolidate Duplicate Code / Extract Common Styles** |
| `Update index.html` | Додано атрибут `lang` для HTML-документу | **Introduce Semantic Attribute / Improve Accessibility** |
| `Create scripts/generate_report.sh and update .pre-commit-config.yaml` | Додано автоматичне формування звіту статичного аналізу; покращено pre-commit конфігурацію | **Introduce Automation Script / Replace Manual Task with Script** |
| `Test flake8 report #61` | Налаштовано правильний запуск flake8 через pre-commit, виправлено шляхи і дублікати | **Refactor Build Script / Simplify Configuration** |
| `fix django env name` | Виправлено неправильну назву змінної середовища | **Rename Variable** |
| `reeplace color with another already used on site` | Замінено кольори у CSS для узгодженості стилю | **Introduce Constant / Unify Style Variables** |

---

##  Key Improvements

- **CSS**: зменшено кількість дублюючих стилів, покращено узгодженість кольорів і класів.  
- **HTML**: додано `lang` для кращої доступності.  
- **Backend**: виправлено docker-команди та pre-commit скрипти, що раніше дублювалися.  
- **Scripts**: створено автоматичне формування звітів (`generate_report.sh`), замінено ручні дії автоматичними.  
- **JS**: підвищено надійність і сумісність (використано `Number.parseFloat`, `globalThis`, optional chaining).

---

## Results

Після рефакторингу:
- Всі **SonarCloud warnings усунено**.  
- Всі **автоматизовані тести пройшли успішно**.  
- Код став **коротшим, чистішим і більш підтримуваним**.
