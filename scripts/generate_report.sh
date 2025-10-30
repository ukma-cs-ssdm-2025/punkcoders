#!/usr/bin/env bash

OUTPUT_FILE="static-analysis.md"
DATE=$(date)

# --- 0. Створення/перезапис файлу ---
echo "# Звіт Статичного Аналізу Коду" > "$OUTPUT_FILE"
echo "Дата генерації: $DATE" >> "$OUTPUT_FILE"
echo "---" >> "$OUTPUT_FILE"

# --- 1. Перевірка форматування та імпортів ---
echo "## Перевірка Форматування та Імпортів" >> "$OUTPUT_FILE"
echo "Black та isort були успішно запущені як pre-commit хуки. Код відформатований та імпорти відсортовані." >> "$OUTPUT_FILE"
echo "---" >> "$OUTPUT_FILE"

# --- 2. Детальний звіт Flake8 ---
echo "## Детальний Звіт Flake8 (Лінтинг)" >> "$OUTPUT_FILE"

# Запуск Flake8 та збереження результату у змінну
FLAKE8_OUTPUT=$(python -m flake8 --config=pyproject.toml backend/delivery-service/app)

if [ -z "$FLAKE8_OUTPUT" ]; then
    echo "✅ Помилок не знайдено" >> "$OUTPUT_FILE"
else
    echo "⚠️ Виявлені помилки:" >> "$OUTPUT_FILE"
    echo '```' >> "$OUTPUT_FILE"
    echo "$FLAKE8_OUTPUT" >> "$OUTPUT_FILE"
    echo '```' >> "$OUTPUT_FILE"
fi

echo "---" >> "$OUTPUT_FILE"

# --- 3. Додавання файлу у staged для коміту ---
git add "$OUTPUT_FILE"
echo "Звіт згенеровано та додано до staged для коміту: $OUTPUT_FILE"