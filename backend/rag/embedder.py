"""
Geração de embeddings com fallback automático:
  1. sentence-transformers (BERT) — melhor qualidade semântica
  2. TF-IDF via sklearn        — fallback se torch não carregar
"""
import logging
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from backend.config import EMBEDDING_MODEL

logger = logging.getLogger("jarvis.embedder")

_bert_model = None
_tfidf_vectorizer: TfidfVectorizer | None = None
_use_bert: bool | None = None   # None = ainda não decidido


def _try_load_bert() -> bool:
    global _bert_model, _use_bert
    if _use_bert is not None:
        return _use_bert
    try:
        from sentence_transformers import SentenceTransformer
        _bert_model = SentenceTransformer(EMBEDDING_MODEL)
        _use_bert = True
        logger.info("[Embedder] BERT carregado: %s", EMBEDDING_MODEL)
    except Exception as exc:
        _use_bert = False
        logger.warning("[Embedder] BERT indisponível (%s). Usando TF-IDF.", exc)
    return _use_bert


# ── API pública ───────────────────────────────────────────────────────────────

def fit(texts: list[str]) -> None:
    """Treina o TF-IDF no corpus completo (chamado uma vez no build_index)."""
    if not _try_load_bert():
        global _tfidf_vectorizer
        _tfidf_vectorizer = TfidfVectorizer(
            max_features=8000,
            ngram_range=(1, 2),
            sublinear_tf=True,
        )
        _tfidf_vectorizer.fit(texts)
        logger.info("[Embedder] TF-IDF treinado com %d documentos.", len(texts))


def embed_texts(texts: list[str]) -> np.ndarray:
    """Gera vetores para uma lista de textos. Retorna array (N, dim)."""
    if _use_bert:
        return _bert_model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
    return _tfidf_vectorizer.transform(texts).toarray().astype("float32")


def embed_query(query: str) -> np.ndarray:
    """Gera vetor para a query. Retorna array (dim,)."""
    if _use_bert:
        return _bert_model.encode([query], convert_to_numpy=True, show_progress_bar=False)[0]
    return _tfidf_vectorizer.transform([query]).toarray()[0].astype("float32")


def backend_name() -> str:
    return "BERT" if _use_bert else "TF-IDF"
