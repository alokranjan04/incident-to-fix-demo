"""Inventory routes."""
from fastapi import APIRouter, HTTPException

from app.models import ProductPublic
from app.services import inventory

router = APIRouter(prefix="/inventory", tags=["inventory"])


@router.get("/low-stock")
def low_stock(threshold: int = 5):
    return [ProductPublic(**p.model_dump()) for p in inventory.low_stock(threshold)]


@router.get("/{item_id}")
def get_item(item_id: str):
    product = inventory.get_product(item_id)
    if product is None:
        raise HTTPException(status_code=404, detail="item not found")
    return product
