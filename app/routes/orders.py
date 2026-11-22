"""Order routes."""
from fastapi import APIRouter, HTTPException

from app.models import Order, OrderCreate
from app.services import inventory, pricing
from app.store import ORDERS, next_order_id

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("")
def list_orders(status: str | None = None, limit: int = 20, offset: int = 0):
    """List orders, newest last, optionally filtered by status."""
    items = list(ORDERS.values())
    if status:
        items = [o for o in items if o.status == status]
    return items[offset : offset + limit]


@router.get("/{order_id}")
def get_order(order_id: int):
    order = ORDERS.get(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="order not found")
    return order


@router.post("", status_code=201)
def create_order(order: OrderCreate):
    """Create an order: check the item, reserve stock, then price it."""
    product = inventory.get_product(order.item_id)
    if product is None:
        raise HTTPException(status_code=404, detail="item not found")
    if not inventory.reserve(order.item_id, order.quantity):
        raise HTTPException(status_code=409, detail="not enough stock")

    try:
        total = pricing.order_total(product.price, order.quantity, order.coupon)
    except ValueError as exc:
        inventory.release(order.item_id, order.quantity)
        raise HTTPException(status_code=400, detail=str(exc))
    unit_price = total / order.quantity
    new_order = Order(
        order_id=next_order_id(),
        item_id=product.item_id,
        quantity=order.quantity,
        unit_price=round(unit_price, 2),
        total=total,
    )
    ORDERS[new_order.order_id] = new_order
    return new_order


@router.post("/{order_id}/cancel")
def cancel_order(order_id: int):
    order = ORDERS.get(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="order not found")
    if order.status == "SHIPPED":
        raise HTTPException(status_code=409, detail="shipped orders cannot be cancelled")
    if order.status != "CANCELLED":
        order.status = "CANCELLED"
    return order


@router.post("/{order_id}/ship")
def ship_order(order_id: int):
    order = ORDERS.get(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="order not found")
    if order.status != "PLACED":
        raise HTTPException(status_code=409, detail="only placed orders can be shipped")
    order.status = "SHIPPED"
    return order
