import numpy as np
from backend.config import EMBEDDING_MODEL

_model = None


def _get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model


def embed_texts(texts: list[str]) -> np.ndarray:
    """Gera embeddings BERT para uma lista de textos. Retorna array (N, dim)."""
    return _get_model().encode(texts, convert_to_numpy=True, show_progress_bar=False)


def embed_query(query: str) -> np.ndarray:
    """Gera embedding para uma query. Retorna array (dim,)."""
    return _get_model().encode([query], convert_to_numpy=True, show_progress_bar=False)[0]
