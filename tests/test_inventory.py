def test_get_item_by_id(client):
    r = client.get("/inventory/A100")
    assert r.status_code == 200
    assert r.json()["name"] == "Notebook"


def test_missing_item_is_404(client):
    assert client.get("/inventory/Z999").status_code == 404


def test_low_stock_default_threshold(client):
    ids = sorted(p["item_id"] for p in client.get("/inventory/low-stock").json())
    assert ids == ["B200", "C300"]
