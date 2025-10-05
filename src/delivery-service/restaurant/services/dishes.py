
def get_all_dishes():
	"""TODO: Stub business logic — returns hardcoded example data."""
	return [
		{"id": 1, "name": "Pizza Margherita", "price": 9.99, "is_available": True},
		{"id": 2, "name": "Pasta Carbonara", "price": 10.50, "is_available": False},
	]

def has_dish(dish_id):
	return any(d["id"] == dish_id for d in get_all_dishes())

def get_dish_by_id(pk):
	return next((d for d in get_all_dishes() if str(d["id"]) == str(pk)), None)

def create_dish(data):
	"""TODO: Stub business logic — creates nothing and returns a mock ID."""
	data["id"] = 999
	return data

def update_dish(dish_id, data):
	return data

def delete_dish(dish_id):
	pass