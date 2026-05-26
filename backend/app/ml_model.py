from .embeddings import index_ticket, search_similar
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

# Minimal classifier + index integration
_model = None


def train_dummy():
    global _model
    texts = ["account issue", "payment failed", "bug in app", "feature request"]
    labels = ["account", "payment", "bug", "feature"]
    _model = make_pipeline(TfidfVectorizer(), LogisticRegression())
    _model.fit(texts, labels)


def predict_text(text: str) -> str:
    global _model
    if _model is None:
        train_dummy()
    pred = _model.predict([text])[0]
    return pred


def add_to_index(ticket_id: int, text: str):
    try:
        index_ticket(ticket_id, text)
    except Exception:
        pass


def similar_tickets(text: str, k: int = 5):
    try:
        return search_similar(text, k)
    except Exception:
        return []
