import pytest
from django.apps import apps


@pytest.mark.django_db
def test_restaurant_app_registered():
    assert apps.is_installed("restaurant")


def test_admin_login_page_accessible(client):
    resp = client.get("/admin/login/")
    assert resp.status_code == 200


def test_openapi_schema_available(client):
    # DRF Spectacular schema endpoint
    resp = client.get("/api/v0/schema/")
    assert resp.status_code == 200
    # у JSON має бути поле "openapi" або в YAML — текст
    content_type = resp.headers.get("Content-Type", "")
    assert "application/json" in content_type or "application/vnd.oai.openapi" in content_type or "yaml" in content_type
