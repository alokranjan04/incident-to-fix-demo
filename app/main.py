"""Demo order service used as the target repo for the incident-to-fix agent."""
from fastapi import FastAPI

from app.routes import inventory, orders

app = FastAPI(title="Order Service (incident-to-fix demo)")
app.include_router(orders.router)
app.include_router(inventory.router)


@app.get("/health")
def health():
    return {"status": "ok"}
