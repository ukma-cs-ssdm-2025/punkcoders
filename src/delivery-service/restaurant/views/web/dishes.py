from django.shortcuts import render, get_object_or_404
from django.http import Http404

# Припускаємо, що ваш service.py знаходиться тут
from restaurant.services import dishes as dish_service

# ----------------------------------------------------------------------
# 1. Список страв (Dish List View)
# FR-001: Домашня сторінка відображає повний список страв.
# US-002: Підтримка пошуку, фільтрації та сортування через параметри GET.
# ----------------------------------------------------------------------
def dish_list(request):
    """
    Відображає список усіх доступних страв, застосовуючи фільтри та сортування 
    на основі GET-параметрів (запиту користувача).
    """
    category_slug = request.GET.get('category')
    search_term = request.GET.get('q')
    sort_by = request.GET.get('sort', 'name')
    
    # Отримання списку страв через сервісний шар
    # Примітка: Логіку has_ingredients та lacks_ingredients ми поки ігноруємо у view, 
    # оскільки вона вимагає складнішого парсингу ID.
    dishes = dish_service.get_dishes(
        category_slug=category_slug,
        search_term=search_term,
        sort_by=sort_by
        # has_ingredients=..., 
        # lacks_ingredients=...
    )

    context = {
        'dishes': dishes,
        'current_category': category_slug,
        'current_search': search_term,
        'current_sort': sort_by,
    }
    
    return render(request, 'dishes/dish_list.html', context)

# ----------------------------------------------------------------------
# 2. Деталі страви (Dish Detail View)
# ----------------------------------------------------------------------
def dish_detail(request, pk):
    """
    Відображає деталі однієї страви за її первинним ключем (ID).
    """
    dish = dish_service.get_dish_by_id(pk)
    if dish is None:
        raise Http404("Страва не знайдена або недоступна")  
    return render(request, 'dishes/dish_detail.html', dish)