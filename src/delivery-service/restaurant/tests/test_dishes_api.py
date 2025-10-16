from rest_framework import status
from rest_framework.test import APITestCase

BASE = "/api/v0/dishes/"


class DishesApiTests(APITestCase):

    def test_list_returns_200_and_array(self):
        resp = self.client.get(BASE)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIsInstance(resp.json(), list)

    def test_retrieve_nonexistent_returns_404(self):
        resp = self.client.get(f"{BASE}999999/")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    # def test_create_valid_returns_201_and_body(self):
    #     payload = {"name": "Pizza Margherita", "price": 9.99, "is_available": True}
    #     resp = self.client.post(BASE, data=payload, format="json")
    #     self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
    #     body = resp.json()
    #     self.assertIn("id", body)
    #     self.assertEqual(body["name"], payload["name"])
    #     self.assertEqual(float(body["price"]), payload["price"])
    #     self.assertEqual(body["is_available"], payload["is_available"])

    # def test_create_invalid_returns_400(self):
    #     payload = {"price": -1, "is_available": True}
    #     resp = self.client.post(BASE, data=payload, format="json")
    #     self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertIsInstance(resp.json(), dict)

    # def test_update_nonexistent_returns_404(self):
    #     payload = {"name": "Updated", "price": 123.0, "is_available": False}
    #     resp = self.client.put(f"{BASE}999999/", data=payload, format="json")
    #     self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    # def test_delete_nonexistent_returns_404(self):
    #     resp = self.client.delete(f"{BASE}999999/")
    #     self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_returns_401(self):
        payload = {"name": "Pizza Margherita", "price": 9.99, "is_available": True}
        resp = self.client.post(BASE, data=payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_returns_401(self):
        payload = {"name": "Updated", "price": 123.0, "is_available": False}
        resp = self.client.put(f"{BASE}1/", data=payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_returns_401(self):
        resp = self.client.delete(f"{BASE}1/")
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
