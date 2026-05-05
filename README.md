# Feedback service

FastAPI app for `[Tanya_Feedback]` (feedback entries and summaries). Port **8003**.

Split from the [monorepo](../Azure/README.md). Related repos: [inventory-service](https://github.com/tatsiana-halaburda/inventory-service), [ordering-service](https://github.com/tatsiana-halaburda/ordering-service).

## Business logic

Pure rules live in [`services/feedback/domain.py`](services/feedback/domain.py): rating distribution (1–5), weighted average, and duplicate detection in a time window. [`services/feedback/main.py`](services/feedback/main.py) uses `domain` before inserts and for read-only aggregates.

**New endpoint:** `GET /feedback/{ingredient_id}/distribution` — histogram of non-archived ratings, weighted average, and total count.

`POST /feedback` rejects duplicate submissions: same `ingredient_id` and `source` within a **5-minute** window returns **409**.

## Environment

Copy [`.env.example`](.env.example) → `.env`. Database credentials only (no Service Bus in this service). [`docker-compose.yml`](docker-compose.yml) uses `${VAR:-…}` from `.env` for compose-time substitution.

## Azure SQL

Run `sql/01_schemas.sql` through `sql/05_seed.sql` in order (shared DB).

## Run

```bash
docker compose up --build -d
```

Local:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn services.feedback.main:app --host 127.0.0.1 --port 8003
```

OpenAPI: `http://127.0.0.1:8003/docs`

## Tests and lint (local)

```bash
pip install -r requirements.txt -r requirements-dev.txt
ruff check .
pytest tests/ -v --tb=short
```

- `tests/test_smoke.py` — OpenAPI smoke (no DB).
- `tests/test_domain.py` — unit tests for `services.feedback.domain`.

## CI (Azure Pipelines)

Pipeline definition: [`azure-pipelines.yml`](azure-pipelines.yml). On push or PR to `main` it runs **Ruff** then **Pytest**. In Azure DevOps, create a pipeline from this file at the repo root. Optional variables match `.env.example` for future integration tests.
