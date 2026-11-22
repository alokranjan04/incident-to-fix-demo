"""In-memory store. Good enough for a demo; reset() gives tests a clean slate."""
from app.models import Order, Product

PRODUCTS: dict[str, Product] = {}
ORDERS: dict[int, Order] = {}
_counter = 0


def next_order_id() -> int:
    global _counter
    _counter += 1
    return _counter


def reset() -> None:
    global _counter
    _counter = 0
    ORDERS.clear()
    PRODUCTS.clear()
    PRODUCTS.update(
        {
            "A100": Product(item_id="A100", name="Notebook", price=120.0, cost_price=70.0, stock=10),
            "B200": Product(item_id="B200", name="Desk lamp", price=899.0, cost_price=540.0, stock=3),
            "C300": Product(item_id="C300", name="Backpack", price=1499.0, cost_price=900.0, stock=1),
        }
    )


reset()
