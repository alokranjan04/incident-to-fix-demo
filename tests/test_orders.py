def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_create_order_prices_with_tax(client):
    r = client.post("/orders", json={"item_id": "A100", "quantity": 2})
    assert r.status_code == 201
    body = r.json()
    assert body["total"] == 252.0  # 2 x 120 + 5% tax
    assert body["unit_price"] == 126.0


def test_zero_quantity_is_400(client):
    r = client.post("/orders", json={"item_id": "A100", "quantity": 0})
    assert r.status_code == 400
    assert r.json()["detail"] == "quantity must be at least 1"


def test_unknown_item_is_404(client):
    assert client.post("/orders", json={"item_id": "Z999", "quantity": 1}).status_code == 404


def test_not_enough_stock_is_409(client):
    assert client.post("/orders", json={"item_id": "B200", "quantity": 4}).status_code == 409


def test_get_order(client):
    order_id = client.post("/orders", json={"item_id": "A100", "quantity": 1}).json()["order_id"]
    assert client.get(f"/orders/{order_id}").json()["item_id"] == "A100"


def test_ship_then_list_by_status(client):
    order_id = client.post("/orders", json={"item_id": "A100", "quantity": 1}).json()["order_id"]
    client.post(f"/orders/{order_id}/ship")
    shipped = client.get("/orders", params={"status": "SHIPPED"}).json()
    assert [o["order_id"] for o in shipped] == [order_id]
