
def get_all_dishes():
	"""TODO: Stub business logic — returns hardcoded example data."""
	return [
		{"id": 1, "name": "Pizza Margherita", "price": 9.99, "is_available": True},
		{"id": 2, "name": "Pasta Carbonara", "price": 10.50, "is_available": False},
	]

def has_dish(pk):
	try:
		pk = int(pk)
	except (ValueError, TypeError):
		return False
	return any(d["id"] == pk for d in get_all_dishes())

def get_dish_by_id(pk):
	try:
		pk = int(pk)
	except (ValueError, TypeError):
		return None
	print(type(pk))
	return next((d for d in get_all_dishes() if d["id"] == pk), None)

def create_dish(data):
	"""TODO: Stub business logic — creates nothing and returns a mock ID."""
	data["id"] = 999
	return data

def update_dish(pk, data):
	data["id"] = pk
	return data

def delete_dish(pk):
	pass