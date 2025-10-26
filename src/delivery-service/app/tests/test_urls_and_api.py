import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api():
    return APIClient()


@pytest.mark.django_db
def test_dishes_list_works(api):
    r = api.get("/api/v0/dishes/")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


@pytest.mark.django_db
def test_dishes_detail_404_when_absent(api):
    r = api.get("/api/v0/dishes/999999/")
    assert r.status_code == 404


@pytest.mark.django_db
def test_dishes_methods_not_allowed(api):
    # ReadOnlyModelViewSet має повертати 405
    assert api.post("/api/v0/dishes/", data={"name": "X"}, format="json").status_code == 401
    assert api.patch("/api/v0/dishes/1/", data={"name": "Y"}, format="json").status_code == 401
    assert api.delete("/api/v0/dishes/1/").status_code == 401
