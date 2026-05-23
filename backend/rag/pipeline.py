"""
Ponto de entrada único para o RAG.
Inicializado uma vez no startup da aplicação; usado pelo rag_tool.
"""
import json
import numpy as np

from backend.config import DATA_DIR, CHUNKS_CACHE, TOP_K
from backend.rag.loader import load_documents
from backend.rag.chunker import chunk_documents
from backend.rag.embedder import embed_texts, embed_query
from backend.rag.retriever import retrieve

_chunks: list[dict] = []
_chunk_vecs: np.ndarray | None = None


def build_index() -> None:
    """Carrega documentos, gera chunks e embeddings. Cacheia em disco."""
    global _chunks, _chunk_vecs

    if CHUNKS_CACHE.exists():
        cached = json.loads(CHUNKS_CACHE.read_text(encoding="utf-8"))
        _chunks = cached["chunks"]
        _chunk_vecs = np.array(cached["vectors"], dtype="float32")
        print(f"[RAG] Índice carregado do cache: {len(_chunks)} chunks")
        return

    print("[RAG] Construindo índice do zero…")
    docs = load_documents(DATA_DIR)
    _chunks = chunk_documents(docs)
    texts = [c["text"] for c in _chunks]
    _chunk_vecs = embed_texts(texts).astype("float32")

    CHUNKS_CACHE.parent.mkdir(parents=True, exist_ok=True)
    CHUNKS_CACHE.write_text(
        json.dumps({"chunks": _chunks, "vectors": _chunk_vecs.tolist()}, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"[RAG] Índice construído e salvo: {len(_chunks)} chunks")


def search(query: str, top_k: int = TOP_K) -> list[dict]:
    """Busca os top_k chunks mais relevantes para a query."""
    if _chunk_vecs is None:
        raise RuntimeError("RAG index não inicializado. Chame build_index() primeiro.")
    q_vec = embed_query(query)
    return retrieve(q_vec, _chunk_vecs, _chunks, top_k)
