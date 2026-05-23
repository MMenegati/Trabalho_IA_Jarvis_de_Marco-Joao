"""Testes da camada RAG: loader, chunker, pipeline de busca."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.rag.loader import load_documents
from backend.rag.chunker import chunk_documents
from backend.config import DATA_DIR, CHUNK_SIZE, CHUNK_OVERLAP


def test_loader_finds_documents():
    docs = load_documents(DATA_DIR)
    assert len(docs) >= 10, f"Esperado >= 10 documentos, encontrado {len(docs)}"


def test_loader_documents_have_text():
    docs = load_documents(DATA_DIR)
    for doc in docs:
        assert "text" in doc and len(doc["text"]) > 100, f"Documento {doc['filename']} com texto curto"


def test_chunker_produces_chunks():
    docs = load_documents(DATA_DIR)
    chunks = chunk_documents(docs)
    assert len(chunks) > 0, "Chunker não gerou chunks"


def test_chunker_chunk_size():
    docs = [{"filename": "test.txt", "text": " ".join(["palavra"] * 500)}]
    chunks = chunk_documents(docs)
    for chunk in chunks[:-1]:  # último pode ser menor
        word_count = len(chunk["text"].split())
        assert word_count <= CHUNK_SIZE, f"Chunk com {word_count} palavras excede CHUNK_SIZE={CHUNK_SIZE}"


def test_chunker_overlap():
    docs = [{"filename": "test.txt", "text": " ".join([str(i) for i in range(400)])}]
    chunks = chunk_documents(docs)
    if len(chunks) >= 2:
        end_words_first = set(chunks[0]["text"].split()[-CHUNK_OVERLAP:])
        start_words_second = set(chunks[1]["text"].split()[:CHUNK_OVERLAP])
        overlap = end_words_first & start_words_second
        assert len(overlap) > 0, "Chunks consecutivos não compartilham overlap"


def test_chunker_ids_are_unique():
    docs = load_documents(DATA_DIR)
    chunks = chunk_documents(docs)
    ids = [c["id"] for c in chunks]
    assert len(ids) == len(set(ids)), "IDs de chunks não são únicos"


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try:
                fn()
                print(f"  PASS  {name}")
            except AssertionError as e:
                print(f"  FAIL  {name}: {e}")
