from backend.rag import pipeline


def buscar_material_rag(query: str) -> str:
    results = pipeline.search(query)
    if not results:
        return "Nenhum trecho relevante encontrado para essa consulta."

    lines = [f"Trechos recuperados para '{query}':"]
    for i, r in enumerate(results, 1):
        lines.append(f"\n[{i}] Fonte: {r['source']} (score: {r['score']:.3f})")
        lines.append(r["text"])
    return "\n".join(lines)
