import os
from celery import Celery

os.environ.setdefault('REDIS_URL', 'redis://redis:6379/0')
redis_url = os.environ.get('REDIS_URL')

celery_app = Celery('backend', broker=redis_url, backend=redis_url)


@celery_app.task
def process_ticket(ticket_id: int):
    # Simple processing: load ticket, run ML prediction and update
    try:
        from backend.app.database import get_session
        from backend.app.models import Ticket
        from backend.app.ml_model import predict_text

        with get_session() as session:
            ticket = session.get(Ticket, ticket_id)
            if not ticket:
                return None
            ticket.category = predict_text(ticket.text)
            session.add(ticket)
            session.commit()
            return ticket.category
    except Exception:
        return None
