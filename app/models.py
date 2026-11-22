"""Data models for orders and products."""
from pydantic import BaseModel


class Product(BaseModel):
    item_id: str
    name: str
    price: float
    cost_price: float  # internal only: never return this to customers
    stock: int


class ProductPublic(BaseModel):
    item_id: str
    name: str
    price: float
    stock: int


class OrderCreate(BaseModel):
    item_id: str
    quantity: int
    coupon: str | None = None


class Order(BaseModel):
    order_id: int
    item_id: str
    quantity: int
    unit_price: float
    total: float
    status: str = "PLACED"
