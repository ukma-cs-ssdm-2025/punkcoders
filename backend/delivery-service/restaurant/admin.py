from django.contrib import admin

from .models import Category, Dish, DishIngredient, Ingredient


# Клас для керування Інгредієнтами
class IngredientAdmin(admin.ModelAdmin):
    # Цей рядок виправляє помилку Admin.E040
    search_fields = ["name"]
    list_display = ("name",)


# Клас для вбудованого редагування інгредієнтів
class DishIngredientInline(admin.TabularInline):
    model = DishIngredient
    extra = 1  # Кількість порожніх форм для додавання
    autocomplete_fields = ["ingredient"]  # Дозволяє шукати інгредієнти


# Налаштування вигляду моделі Dish
class DishAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "category", "is_available")
    list_filter = ("category", "is_available")
    search_fields = ("name", "description")
    inlines = [DishIngredientInline]  # Додаємо можливість керувати інгредієнтами тут же


# Налаштування вигляду моделі Category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_alcoholic")
    # prepopulated_fields = {"slug": ("name",)}  # Автоматично генерує slug з назви


# Реєстрація моделей в Admin Panel
admin.site.register(Category, CategoryAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Dish, DishAdmin)
