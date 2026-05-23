import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from backend.config import TOP_K


def retrieve(query_vec: np.ndarray, chunk_vecs: np.ndarray,
             chunks: list[dict], top_k: int = TOP_K) -> list[dict]:
    """Retorna os top_k chunks mais similares à query."""
    scores = cosine_similarity([query_vec], chunk_vecs)[0]
    top_indices = np.argsort(scores)[::-1][:top_k]
    results = []
    for i in top_indices:
        results.append({
            **chunks[i],
            "score": float(scores[i]),
        })
    return results
