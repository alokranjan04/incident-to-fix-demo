# incident-to-fix-demo

A small FastAPI order service. It is the **target repo** for the
[incident-to-fix agent](../incident-to-fix-agent): ServiceNow incidents describe bugs in
this service, and the agent opens pull requests that fix them.

## Run it

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload       # http://127.0.0.1:8000/docs
pytest -q
```

## Endpoints

| Method | Path | What it does |
| --- | --- | --- |
| GET | /health | Liveness check |
| POST | /orders | Create an order (checks stock, applies coupon, adds 5% tax) |
| GET | /orders | List orders (`status`, `limit`, `offset`) |
| GET | /orders/{id} | Get one order |
| POST | /orders/{id}/ship | Mark an order shipped |
| POST | /orders/{id}/cancel | Cancel an order and return its stock |
| GET | /inventory/{item_id} | Public product info |
| GET | /inventory/low-stock | Products below a stock threshold |

## Known issue

`main` contains a real bug reported as ServiceNow incident INC0010004.
Further bugs live on `bug/NN` branches for the agent's evaluation runs.
