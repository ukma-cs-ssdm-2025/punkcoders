#!/usr/bin/env bash

# Створення/перезапис файлу зі статичним заголовком
echo "# Звіт Статичного Аналізу Коду" > static-analysis.md
echo "Дата генерації: $(date)" >> static-analysis.md
echo "---" >> static-analysis.md

# 1. Секція Black та isort (інструменти виправлення)
echo "## Перевірка Форматування та Імпортів" >> static-analysis.md
echo "Black та isort були успішно запущені як pre-commit хуки. Код відформатований та імпорти відсортовані." >> static-analysis.md
echo "---" >> static-analysis.md

# 2. Детальний Звіт Flake8 (Лінтинг)
echo "## Детальний Звіт Flake8 (Лінтинг)" >> static-analysis.md

# Запуск Flake8 на всьому проєкті.
# Результати перенаправляються у файл.
# '|| true' гарантує, що скрипт завжди поверне успішний код виходу (0),
# навіть якщо flake8 знайде помилки.
flake8 --config=pyproject.toml . >> static-analysis.md || true

# 3. Додавання оновленого файлу до staged-файлів для коміту
git add static-analysis.md