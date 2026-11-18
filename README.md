# coding-test-python-backend

## Running the Application

To run the FastAPI development server:

```bash
uvicorn app.main:app --reload
```

## Running Tests

To run the test suite:

```bash
pytest
```

## Knowledge Graph (Graphify)

This repository is indexed with **Graphify** to support code and architecture knowledge graph queries.
- Graph artifacts are located in `graphify-out/` (`graph.json`, `graph.html`, and `GRAPH_REPORT.md`).
- Assistant rules, workflows, and skills are configured in `.agents/`.

### Update Command

To update the knowledge graph after modifying code files (AST-only, fast, no LLM needed):

```bash
graphify update .
```

*(Alternatively, to force update if nodes/files were deleted: `graphify update . --force`)*

## Design Decisions

- **Graphify CLI Isolation:** `graphifyy` is installed as a standalone CLI tool via `uv tool install graphifyy` because Graphify requires Python 3.10+, keeping the application virtualenv (Python 3.9) clean and focused strictly on the FastAPI backend dependencies.
- **Project-scoped Agent Configuration:** Configured Graphify skills, workflows, and rules under `.agents/` (`.agents/skills/graphify`, `.agents/rules/graphify.md`, and `.agents/workflows/graphify.md`) so that any AI assistant working in this workspace can navigate architecture and graph queries directly.
- **In-memory storage via module-level dict:** `_shipments: dict[str, ShipmentOut]` lives in `app/services/shipment_service.py`. No database setup is needed; data is lost on server restart by design. A `clear_all()` helper allows per-test isolation without dependency injection overhead.
- **`ShipmentStatus` as `str, Enum`:** Using a `str` subclass enum gives free 422 validation on both PATCH body and `?status=` query parameter — no manual checking needed in route handlers.
- **`@pytest_asyncio.fixture` for async fixtures:** `pytest-asyncio` runs in strict mode, requiring async fixtures to be declared with `@pytest_asyncio.fixture` (not `@pytest.fixture`) to be properly awaited by the framework.
