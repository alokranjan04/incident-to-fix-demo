"""Pricing rules: coupons first, then tax."""

COUPONS = {"SAVE10": 0.10, "SAVE25": 0.25}
TAX_RATE = 0.05


def apply_coupon(subtotal: float, coupon: str | None) -> float:
    if not coupon:
        return subtotal
    pct = COUPONS.get(coupon.upper())
    if pct is None:
        raise ValueError(f"unknown coupon {coupon}")
    return subtotal * (1 - pct)


def order_total(price: float, quantity: int, coupon: str | None = None) -> float:
    subtotal = price * quantity
    discounted = apply_coupon(subtotal, coupon)
    return float(int(discounted * (1 + TAX_RATE)))
