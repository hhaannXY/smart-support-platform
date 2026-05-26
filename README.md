# Smart Support Platform (Demo)

Коротко: демонстрационный проект для автоматизации техподдержки — показывает backend (FastAPI), ML‑инфраструктуру, интеграцию с Telegram, и фронтенд на React. Отлично подходит для показа навыков backend/frontend/ML/DevOps в портфолио.

Features
- FastAPI backend с REST API
- ML‑модуль (классификатор заявок + поиск похожих)
- Telegram‑бот для приёма заявок и уведомлений (токен через переменную окружения)
- React + Vite фронтенд (панель операторов)
- Docker + docker‑compose, GitHub Actions CI

Quick start (локально)

1) Создать виртуальное окружение и установить зависимости:

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

2) Запустить backend (dev):

```bash
set TELEGRAM_TOKEN=your_token_here  # Windows
uvicorn backend.app.main:app --reload
```

3) Фронтенд:

```bash
cd frontend
npm install
npm run dev
```

Docker demo (docker-compose):

```bash
docker compose up --build
```

Security note: не выкладывайте токен Telegram публично. Добавляйте его в secrets при деплое.

What is this project?
- Это служба поддержки с backend на FastAPI, frontend на React, Telegram-ботом и живыми обновлениями.
- Telegram-бот пересылает сообщения в backend, backend хранит заявки и классифицирует их, frontend показывает заявки в реальном времени.

Running locally
1) Backend + dependencies:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```
2) Frontend:
```bash
cd frontend
npm install
npm run dev
```
3) Backend server:
```bash
set DATABASE_URL=sqlite:///./dev.db
set REDIS_URL=redis://localhost:6379/0
set TELEGRAM_TOKEN=your_token_here
uvicorn backend.app.main:app --reload --port 8000
```
Alternatively, create `backend/.env` with your values and start with `run.ps1`:
```powershell
cd project
.\run.ps1
```
4) Open `http://localhost:5173` for the frontend.

Docker compose
```bash
docker compose up --build
```
If you use docker-compose, set `TELEGRAM_TOKEN` in your environment or in a `.env` file.

Telegram
- Добавьте свой токен в `TELEGRAM_TOKEN`.
- Отправьте `/start` боту, затем любой текст — он попадёт в backend через `POST /tickets/submit`.
- В интерфейсе заявки появятся автоматически через WebSocket.

Developer notes
- backend: `backend/app/main.py`, `backend/app/telegram_bot.py`, `backend/app/telegram_bot.py`, `backend/app/ml_model.py`.
- frontend: `frontend/src/App.jsx`, `frontend/vite.config.js`.
- To test: `pytest -q`.

Developer notes
- **Архитектура:** backend (FastAPI) в [backend/app/main.py](backend/app/main.py#L1), модели в [backend/app/models.py](backend/app/models.py#L1), ML‑стабы в [backend/app/ml_model.py](backend/app/ml_model.py#L1), Telegram‑бот в [backend/app/telegram_bot.py](backend/app/telegram_bot.py#L1). Фронтенд — в `frontend/`.
- **Аутентификация:** реализована JWT‑аутентификация. Регистрация — `POST /auth/register`, получение токена — `POST /auth/token` (OAuth2 password flow). Защищённые маршруты требуют заголовка `Authorization: Bearer <token>`.
- **Как объяснить проект на собеседовании:** расскажи про API endpoints, как ML‑модуль классифицирует заявки (покажи `backend/app/ml_model.py`), и как Telegram‑интеграция отправляет сообщения в API; упомяни Celery worker для фоновой обработки.
- **Runbook:** см. [DEV_SETUP.md](DEV_SETUP.md).
