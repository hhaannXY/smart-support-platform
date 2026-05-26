Developer setup and explanation

This document explains how the project is organized, how to run it locally, and talking points to explain the codebase.

Components
- backend/: FastAPI application. Key files:
  - backend/app/main.py — API entrypoint and endpoints.
  - backend/app/models.py — SQLModel model definitions (Ticket).
  - backend/app/schemas.py — Pydantic request/response schemas.
  - backend/app/crud.py — DB helpers (create, read, update, delete).
  - backend/app/ml_model.py — ML stub (train & predict).
  - backend/app/telegram_bot.py — Telegram integration forwarding messages to API.
  - backend/celery_worker.py — Celery task `process_ticket` for background ML processing.

- frontend/: Minimal React (Vite) dashboard that lists tickets and demonstrates a UI.
- docker-compose.yml: local development stack (Postgres, Redis, backend, worker, frontend).

Local development

1. Build & run with Docker Compose (recommended):

```bash
docker compose up --build
```

This starts Postgres, Redis, backend (uvicorn) and a worker (Celery). The backend will expose port 8000.

2. Run migrations (if not using Docker):

```bash
cd backend
pip install -r ../requirements.txt
alembic -c alembic.ini revision --autogenerate -m "init"
alembic -c alembic.ini upgrade head
```

3. Run tests locally:

```bash
pytest -q
```

Explaining the code to interviewers — talking points
- Show the request flow: Telegram -> `telegram_bot` -> POST /tickets -> stored in DB -> Celery task `process_ticket` classifies text and updates ticket.
- Explain ML stub: simple TF‑IDF + LogisticRegression pipeline in `ml_model.py` and where to replace with real model or embeddings.
- Show async & background processing: Celery worker handles CPU/IO heavy work outside request cycle.
- Show infra/deploy: Docker Compose, GitHub Actions for CI, and how you would deploy on Render/Fly/Vercel.

Security
- Never commit the `TELEGRAM_TOKEN` or DB credentials. Use environment variables and GitHub Secrets for CI.
