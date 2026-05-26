from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

from .database import init_db, get_session
from .models import Ticket, User
from .ml_model import predict_text
from .ws import manager as ws_manager, broadcast_new_ticket
from fastapi import WebSocket
from .schemas import TicketCreate, TicketRead, UserCreate, Token
from .crud import create_ticket as crud_create, get_ticket as crud_get, list_tickets as crud_list, update_ticket as crud_update, delete_ticket as crud_delete
from .crud import create_user, authenticate_user
from .auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_current_active_user
from datetime import timedelta
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI(title="Smart Support Platform")

# Allow local frontend during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    # load environment variables from backend/.env when present
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))
    init_db()
    try:
        from ..sentry_init import init_sentry
        init_sentry()
    except Exception:
        pass
    token = os.environ.get("TELEGRAM_TOKEN")
    if token:
        try:
            import asyncio
            from . import telegram_bot
            asyncio.create_task(telegram_bot.start_bot(token))
        except Exception:
            pass


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/tickets", response_model=TicketRead)
def create_ticket(payload: TicketCreate, background_tasks: BackgroundTasks, current_user=Depends(get_current_active_user)):
    # create ticket as authenticated admin action
    with get_session() as session:
        ticket = crud_create(session, payload)

    # If Celery is available, enqueue background processing
    redis_url = os.environ.get("REDIS_URL")
    if redis_url:
        try:
            from .celery_worker import process_ticket
            process_ticket.delay(ticket.id)
        except Exception:
            pass
    else:
        ticket.category = predict_text(ticket.text)
        with get_session() as session:
            session.add(ticket)
            session.commit()

    try:
        import asyncio
        asyncio.create_task(broadcast_new_ticket(TicketRead.from_orm(ticket).dict()))
    except Exception:
        pass
    return TicketRead.from_orm(ticket)


@app.post("/tickets/submit", response_model=TicketRead)
def submit_ticket(payload: TicketCreate):
    # public submission endpoint for Telegram and frontend visitors
    with get_session() as session:
        ticket = crud_create(session, payload)

    ticket.category = predict_text(ticket.text)
    with get_session() as session:
        session.add(ticket)
        session.commit()

    try:
        import asyncio
        asyncio.create_task(broadcast_new_ticket(TicketRead.from_orm(ticket).dict()))
    except Exception:
        pass
    return TicketRead.from_orm(ticket)


@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except Exception:
        ws_manager.disconnect(websocket)


@app.post('/auth/register', response_model=dict)
def register(user: UserCreate):
    with get_session() as session:
        if session.query(User).filter(User.username == user.username).first():
            raise HTTPException(status_code=400, detail="User already exists")
        u = create_user(session, user.username, user.password)
        return {"ok": True, "id": u.id}


@app.post('/auth/token', response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    with get_session() as session:
        user = authenticate_user(session, form_data.username, form_data.password)
        if not user:
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
        return {"access_token": access_token, "token_type": "bearer"}


@app.get("/tickets", response_model=list[TicketRead])
def list_tickets():
    with get_session() as session:
        items = crud_list(session)
        return [TicketRead.from_orm(i) for i in items]


@app.get("/tickets/{ticket_id}", response_model=TicketRead)
def get_ticket(ticket_id: int):
    with get_session() as session:
        t = crud_get(session, ticket_id)
        if not t:
            raise HTTPException(status_code=404, detail="Ticket not found")
        return TicketRead.from_orm(t)


@app.put("/tickets/{ticket_id}", response_model=TicketRead)
def update_ticket(ticket_id: int, payload: TicketCreate):
    with get_session() as session:
        t = crud_update(session, ticket_id, payload)
        if not t:
            raise HTTPException(status_code=404, detail="Ticket not found")
        return TicketRead.from_orm(t)


@app.delete("/tickets/{ticket_id}")
def delete_ticket(ticket_id: int):
    with get_session() as session:
        ok = crud_delete(session, ticket_id)
        if not ok:
            raise HTTPException(status_code=404, detail="Ticket not found")
        return {"ok": True}
