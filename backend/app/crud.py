from .models import Ticket
from .schemas import TicketCreate
from .database import get_session


def create_ticket(session, ticket_in: TicketCreate) -> Ticket:
    ticket = Ticket(text=ticket_in.text)
    session.add(ticket)
    session.commit()
    session.refresh(ticket)
    # index for semantic search
    try:
        from .ml_model import add_to_index
        add_to_index(ticket.id, ticket.text)
    except Exception:
        pass
    return ticket


def get_ticket(session, ticket_id: int):
    return session.get(Ticket, ticket_id)


def list_tickets(session):
    return session.query(Ticket).all()


def update_ticket(session, ticket_id: int, ticket_in: TicketCreate):
    ticket = session.get(Ticket, ticket_id)
    if not ticket:
        return None
    ticket.text = ticket_in.text
    session.add(ticket)
    session.commit()
    session.refresh(ticket)
    return ticket


def delete_ticket(session, ticket_id: int) -> bool:
    ticket = session.get(Ticket, ticket_id)
    if not ticket:
        return False
    session.delete(ticket)
    session.commit()
    return True


# --- User CRUD ---
from passlib.context import CryptContext
from .models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_username(session, username: str):
    return session.query(User).filter(User.username == username).first()


def create_user(session, username: str, password: str) -> User:
    hashed = pwd_context.hash(password)
    user = User(username=username, hashed_password=hashed)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def authenticate_user(session, username: str, password: str):
    user = get_user_by_username(session, username)
    if not user:
        return None
    if not pwd_context.verify(password, user.hashed_password):
        return None
    return user
