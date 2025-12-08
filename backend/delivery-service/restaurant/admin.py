from django.contrib import admin

from .models import Category, Dish, Order, OrderItem


# Налаштування вигляду моделі Dish
class DishAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "category", "is_available")
    list_filter = ("category", "is_available")
    search_fields = ("name", "description")


# Налаштування вигляду моделі Category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_alcoholic")
    # prepopulated_fields = {"slug": ("name",)}  # Автоматично генерує slug з назви


# Реєстрація моделей в Admin Panel
admin.site.register(Category, CategoryAdmin)
admin.site.register(Dish, DishAdmin)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("dish", "name", "unit_price", "quantity", "line_total")
    can_delete = False


class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "total_amount", "phone", "created_at", "self_pickup")
    list_filter = ("status", "self_pickup", "created_at", "payment_method")
    search_fields = ("id", "phone", "delivery_address")
    inlines = [OrderItemInline]
    readonly_fields = ("total_amount", "created_at")


admin.site.register(Order, OrderAdmin)
