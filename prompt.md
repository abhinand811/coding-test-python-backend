# AI Prompt Log — Coding Test
**Candidate Name:** Abhinand N Dev
**Date:** 2026-11-18
**AI Tool(s) Used:** Antigravity (Claude)

---

## Prompt 1
**Prompt:** Please create an AGENTS.md in the repo root with project-level guidelines for any AI agent working here. Cover: the stack and where the code and tests live, clean code standards (type hints, Pydantic models, thin route handlers, proper error handling, async where it makes sense), a testing standard for every endpoint. Keep it concise, practical and easy to scan, with no fluff.

Only create this one file. Don't edit anything else and don't commit. Tell me the path when you're done.
**Helped with:** Created AGENTS.md at the repo root with stack, layout, clean code, and testing standards.

---

## Prompt 2
**Prompt:** Next, I want an always-on workspace rule for this project that enforces the mandatory parts of my coding test.

Please create a rule file at .agent/rules/test-requirements.md  set to always apply. It should make the agent do these things:

- Log every prompt I send into prompt.md, following the template already in that file. It should use my exact wording, never paraphrase, number the entries sequentially, and add a one-line note on what each prompt helped with. It should never backfill entries after the fact.
- Briefly plan before coding, make small changes, and run pytest after each one.
- Keep quality high: no failing tests, no dead code, validate input, and add any new dependency to requirements.txt.
- Keep the bottom of README.md updated with how to run the app, how to run tests, and design decisions.

Keep it short, since long rules slow the agent down. Only create this file. Don't touch prompt.md or anything else, and don't commit.
**Helped with:** Created .agent/rules/test-requirements.md as an always-on workspace rule enforcing prompt logging, workflow discipline, code quality, and README upkeep.

---

## Prompt 3
**Prompt:** Add grphify to this repo and give me the command to update the graphify
**Helped with:** Added graphify to the repository and provided instructions/command to update graphify.

## Prompt 4
**Prompt:** /plan I want to create a shipment tracking system . Keep the following points in context while creating this .

Use FastAPI with in-memory storage (a Python dict or list) — no database
setup required.

The shipment data model should be similar to this 

Field Type Notes
id str (UUID) Auto-generated — not provided by caller
origin str Port of origin, e.g. 'Kochi'
destination str Port of destination, e.g. 'Dubai'
cargo_type str e.g. 'Electronics', 'Machinery'
weight_kg float Must be > 0
status str One of: pending, in_transit, delivered, cancelled
created_at datetime Auto-set to current UTC time on creation


Tasks that to completed as follows 

1. Create a health check api in app/mains.py
2. Create pydantic models  for creating a shipment like this
     – Fields: origin, destination, cargo_type, weight_kg
– weight_kg must be validated — reject values ≤ 0 with a clear error message

and add these values extra to the above data while returning the shipment detail 
 3. Add the following crud apis 
POST /shipments Create a new shipment. Status defaults to 'pending'.
GET /shipments Return all shipments. Support optional ?status= filter.
GET /shipments/{id} Return a single shipment. 404 if not found.
PATCH /shipments/{id}/status Update status only. Validate allowed values.
DELETE /shipments/{id} Delete a shipment. 404 if not found.
**Helped with:** Planning the full shipment tracking system implementation — health check, Pydantic models, CRUD endpoints, in-memory storage, and tests.

## Prompt 5
**Prompt:** Can you add a seeder to fill the entries to this and also give me the curl for these APIs to test
**Helped with:** Added a startup seeder that pre-populates the in-memory store with sample shipments, and provided curl commands for all API endpoints.

## Prompt 6
**Prompt:** Add a filter to this GET /shipments/summary endpoint so that it gives the summary of the shipments based on the status 

expected out :
{
"pending": 3,
"in_transit": 2,
"delivered": 5,
"cancelled": 1,
"total": 11
}
**Helped with:** Added GET /shipments/summary endpoint returning per-status counts and a total, with a ShipmentSummary Pydantic model, service function, route handler, and tests.

## Prompt 7
**Prompt:** I want to add a new logic to this patch API 
PATCH /shipments/{id}/status Update status only. Validate allowed values.
that if the status of the shipment is either delivered or cancelled then the patch should not work and it should return 
HTTP 400 with a descriptive error message
**Helped with:** Added terminal-state guard to PATCH /shipments/{id}/status — returns HTTP 400 when shipment is already delivered or cancelled.

## Prompt 8
**Prompt:** /plan I wanted to do the tests with FastAPI's TestClient.
**Helped with:** Planning migration of the test suite from async HTTPX AsyncClient to FastAPI's synchronous TestClient.
