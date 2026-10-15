"""Tests for the /products CRUD router (story 1)."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.product import Product

PAYLOAD = {"sku": "CHAIR-01", "name": "Wooden chair", "price": "49.90", "stock_qty": 12}


def create_product(api_client: TestClient, **overrides: object) -> dict[str, object]:
    response = api_client.post("/products", json={**PAYLOAD, **overrides})
    assert response.status_code == 201
    return dict(response.json())


# --- create ---


def test_create_returns_201_with_body(api_client: TestClient) -> None:
    body = create_product(api_client)
    assert body["sku"] == "CHAIR-01"
    assert body["name"] == "Wooden chair"
    assert body["price"] == "49.90"
    assert body["stock_qty"] == 12


def test_create_defaults_stock_qty_to_zero(api_client: TestClient) -> None:
    response = api_client.post(
        "/products", json={"sku": "LAMP-02", "name": "Desk lamp", "price": "19.99"}
    )
    assert response.status_code == 201
    assert response.json()["stock_qty"] == 0


def test_create_duplicate_sku_returns_409(api_client: TestClient) -> None:
    create_product(api_client)
    response = api_client.post("/products", json=PAYLOAD)
    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]


@pytest.mark.parametrize(
    "overrides",
    [
        {"name": None},
        {"name": ""},
        {"price": "0"},
        {"price": "-5.00"},
        {"price": "not-a-number"},
        {"sku": None},
        {"stock_qty": -1},
    ],
)
def test_create_validation_errors_return_422(
    api_client: TestClient, overrides: dict[str, object]
) -> None:
    payload = {**PAYLOAD, **overrides}
    response = api_client.post("/products", json=payload)
    assert response.status_code == 422


def test_create_rejects_more_than_two_decimal_places(api_client: TestClient) -> None:
    response = api_client.post("/products", json={"sku": "P1", "name": "n", "price": "10.999"})
    assert response.status_code == 422


# --- read ---


def test_get_by_sku(api_client: TestClient) -> None:
    create_product(api_client)
    response = api_client.get("/products/CHAIR-01")
    assert response.status_code == 200
    assert response.json()["sku"] == "CHAIR-01"


def test_get_unknown_sku_returns_404(api_client: TestClient) -> None:
    response = api_client.get("/products/NOPE")
    assert response.status_code == 404


def test_list_returns_all_products_ordered_by_sku(api_client: TestClient) -> None:
    create_product(api_client)
    api_client.post("/products", json={"sku": "DESK-9", "name": "Desk", "price": "199.00"})
    response = api_client.get("/products")
    assert response.status_code == 200
    assert [p["sku"] for p in response.json()] == ["CHAIR-01", "DESK-9"]


# --- update ---


def test_patch_updates_single_field(api_client: TestClient) -> None:
    create_product(api_client)
    response = api_client.patch("/products/CHAIR-01", json={"name": "Oak chair"})
    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "Oak chair"
    assert body["price"] == "49.90"
    assert body["stock_qty"] == 12


def test_patch_price(api_client: TestClient) -> None:
    create_product(api_client)
    response = api_client.patch("/products/CHAIR-01", json={"price": "59.00"})
    assert response.json()["price"] == "59.00"


def test_patch_unknown_sku_returns_404(api_client: TestClient) -> None:
    response = api_client.patch("/products/NOPE", json={"name": "x"})
    assert response.status_code == 404


def test_patch_rejects_invalid_values(api_client: TestClient) -> None:
    create_product(api_client)
    response = api_client.patch("/products/CHAIR-01", json={"price": "-1"})
    assert response.status_code == 422


# --- delete ---


def test_delete_returns_204_and_removes_product(api_client: TestClient) -> None:
    create_product(api_client)
    assert api_client.delete("/products/CHAIR-01").status_code == 204
    assert api_client.get("/products/CHAIR-01").status_code == 404


def test_delete_unknown_sku_returns_404(api_client: TestClient) -> None:
    response = api_client.delete("/products/NOPE")
    assert response.status_code == 404


# --- service-level, exercises the unique constraint directly ---


def test_unique_constraint_backs_409_at_db_level(db_session: Session) -> None:
    db_session.add(Product(sku="X1", name="n", price="1.00", stock_qty=0))
    db_session.flush()
    db_session.add(Product(sku="X1", name="dup", price="2.00", stock_qty=0))
    with pytest.raises(Exception, match="UNIQUE"):
        db_session.flush()
