"""Stock lookups and reservations."""
from app.models import Product
from app.store import PRODUCTS


def get_product(item_id: str) -> Product | None:
    return PRODUCTS.get(item_id.upper())


def reserve(item_id: str, quantity: int) -> bool:
    product = get_product(item_id)
    if product is None or product.stock <= quantity:
        return False
    product.stock -= quantity
    return True


def release(item_id: str, quantity: int) -> None:
    product = get_product(item_id)
    if product is not None:
        product.stock += quantity


def low_stock(threshold: int) -> list[Product]:
    return [p for p in PRODUCTS.values() if p.stock < threshold]
