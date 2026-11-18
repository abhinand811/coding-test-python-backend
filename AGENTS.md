# AGENTS.md — Project Guidelines for AI Agents

> Read this before touching any code. Follow it strictly; deviations require an explicit comment explaining why.

---

## Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| Server | Uvicorn (via `uvicorn[standard]`) |
| HTTP client | HTTPX |
| Testing | pytest + pytest-asyncio |
| Python | 3.9+ |

---

## Repository Layout

```
.
├── app/
│   ├── __init__.py
│   └── main.py          # FastAPI app instance + route registration
├── tests/
│   └── __init__.py      # test modules go here, mirroring app/ structure
├── requirements.txt
└── AGENTS.md
```

- **Application code** lives under `app/`. Add sub-modules there (e.g. `app/routers/`, `app/services/`, `app/models/`).
- **Tests** live under `tests/`. Mirror the `app/` structure: `app/routers/items.py` → `tests/test_items.py`.
- **Do not** add production code to `tests/` or test helpers to `app/`.

---

## Clean Code Standards

### Type Hints
- Every function signature (parameters **and** return type) must be fully annotated.
- Use `Optional[X]` / `X | None` (Python 3.10+ union syntax is fine), `list[X]`, `dict[K, V]`.
- No bare `Any` unless genuinely unavoidable; add a `# noqa: ANN401` comment if so.

### Pydantic Models
- All request bodies and structured responses use Pydantic `BaseModel`.
- Define models in `app/models/` (or a `schemas.py` module), not inline in route files.
- Use `model_validator` / `field_validator` for business-rule validation; keep validators pure and side-effect-free.

### Route Handlers (keep them thin)
Route handlers must only:
1. Parse / validate input (Pydantic handles this automatically).
2. Call a service or repository function.
3. Return the result or raise an `HTTPException`.

```python
# ✅ Good
@router.post("/items", response_model=ItemOut, status_code=201)
async def create_item(payload: ItemIn, svc: ItemService = Depends(get_item_service)) -> ItemOut:
    return await svc.create(payload)

# ❌ Bad — business logic in the handler
@router.post("/items")
async def create_item(payload: ItemIn):
    if payload.price < 0:
        raise HTTPException(status_code=422, detail="price must be non-negative")
    item = {"id": uuid4(), **payload.dict()}
    db.append(item)
    return item
```

### Error Handling
- Raise `fastapi.HTTPException` with a meaningful `detail` string for expected errors.
- Let unexpected exceptions propagate; add a global exception handler in `main.py` if you need uniform 500 responses.
- Never swallow exceptions silently (`except Exception: pass` is forbidden).
- Validate at the boundary (Pydantic + `HTTPException`); never let raw `ValueError` / `KeyError` escape a handler.

### Async
- Prefer `async def` for all route handlers and any I/O-bound service calls (network, DB, file).
- Use `def` (sync) only for pure CPU-bound helpers that do no I/O.
- Never call blocking I/O (e.g. `requests.get`, `time.sleep`) inside an `async def`; use HTTPX async client or `asyncio.sleep` instead.

---

## Testing Standards

Every endpoint **must** have tests covering at minimum:

| Scenario | What to assert |
|---|---|
| Happy path | Correct status code, response body shape, key field values |
| Invalid input | 422 Unprocessable Entity; meaningful error detail |
| Not found / empty | 404 (or 200 with empty list, whichever the spec says) |
| Edge cases | Boundary values, empty strings, zero, large numbers — whatever applies |

### Setup
```python
# tests/conftest.py
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
```

### Naming
```
test_<verb>_<resource>_<scenario>
# e.g.
test_create_item_success
test_create_item_invalid_price
test_get_item_not_found
```

### Rules
- Mark async tests with `@pytest.mark.asyncio`.
- Do **not** hit external networks in tests; mock or override dependencies via `app.dependency_overrides`.
- Keep each test focused on one scenario; no mega-tests that assert 10 things at once.
- Tests must be runnable with `pytest` from the repo root with no extra setup beyond `pip install -r requirements.txt`.

---

## General Rules
- **No dead code.** Remove commented-out blocks before finishing a task.
- **No print statements** in production paths; use Python `logging` if needed.
- **One concern per module.** Routes, models, and business logic live in separate files.
- **Don't commit secrets.** Use environment variables (`os.getenv`) and `.env` files (gitignored).
