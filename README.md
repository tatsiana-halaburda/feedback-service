# Feedback service

FastAPI app for `[Tanya_Feedback]` (feedback entries and summaries). Port **8003**.

Split from the [monorepo](../Azure/README.md). Related repos: [inventory-service](https://github.com/tatsiana-halaburda/inventory-service), [ordering-service](https://github.com/tatsiana-halaburda/ordering-service).

## Environment

Copy `.env.example` → `.env`. Database credentials only (no Service Bus in this service).

## Azure SQL

Run `sql/01_schemas.sql` through `sql/05_seed.sql` in order (shared DB).

## Run

```bash
docker compose up --build -d
```

Local: `uvicorn services.feedback.main:app --host 127.0.0.1 --port 8003` — OpenAPI `http://127.0.0.1:8003/docs`
