from backend.config import CHUNK_SIZE, CHUNK_OVERLAP


def chunk_documents(docs: list[dict]) -> list[dict]:
    """Divide cada documento em chunks com sliding window."""
    chunks = []
    for doc in docs:
        words = doc["text"].split()
        start = 0
        idx = 0
        while start < len(words):
            end = min(start + CHUNK_SIZE, len(words))
            text = " ".join(words[start:end])
            chunks.append({
                "id": f"{doc['filename']}__chunk{idx}",
                "source": doc["filename"],
                "text": text,
            })
            idx += 1
            if end == len(words):
                break
            start += CHUNK_SIZE - CHUNK_OVERLAP
    return chunks
