import os
from typing import List, Optional
import numpy as np

_encoder = None
_use_faiss = False
_index = None

try:
    from sentence_transformers import SentenceTransformer
    _encoder = SentenceTransformer('all-MiniLM-L6-v2')
except Exception:
    _encoder = None

try:
    import faiss
    _use_faiss = True
except Exception:
    _use_faiss = False


def embed_texts(texts: List[str]):
    if _encoder:
        return np.array(_encoder.encode(texts, convert_to_numpy=True))
    # fallback to simple averaging of ordinals (very naive)
    vecs = []
    for t in texts:
        a = np.frombuffer(t.encode('utf8'), dtype=np.uint8).astype(float)
        if a.size == 0:
            vecs.append(np.zeros(8))
        else:
            # pad or truncate
            if a.size < 8:
                a = np.pad(a, (0, 8 - a.size))
            vecs.append(a[:8])
    return np.vstack(vecs)


class SimpleVectorIndex:
    def __init__(self, dim: int):
        self.dim = dim
        self.items = []
        self.embs = None

    def add(self, id: int, text: str):
        v = embed_texts([text])
        self.items.append((id, text))
        self.embs = v if self.embs is None else np.vstack([self.embs, v])

    def search(self, text: str, k: int = 5):
        if self.embs is None:
            return []
        q = embed_texts([text])[0]
        sims = (self.embs @ q) / (np.linalg.norm(self.embs, axis=1) * (np.linalg.norm(q) + 1e-9))
        idx = np.argsort(-sims)[:k]
        return [(self.items[i][0], float(sims[i])) for i in idx]


_global_index: Optional[SimpleVectorIndex] = None


def ensure_index(dim: int = 384):
    global _global_index
    if _global_index is None:
        _global_index = SimpleVectorIndex(dim)
    return _global_index


def index_ticket(id: int, text: str):
    idx = ensure_index()
    idx.add(id, text)


def search_similar(text: str, k: int = 5):
    idx = ensure_index()
    return idx.search(text, k)
