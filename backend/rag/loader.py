from pathlib import Path


def load_documents(data_dir: Path) -> list[dict]:
    """Carrega todos os .txt e .pdf de data_dir e retorna lista de {filename, text}."""
    docs = []
    for path in sorted(data_dir.glob("*")):
        if path.suffix == ".txt":
            docs.append({"filename": path.name, "text": path.read_text(encoding="utf-8")})
        elif path.suffix == ".pdf":
            text = _load_pdf(path)
            if text.strip():
                docs.append({"filename": path.name, "text": text})
    return docs


def _load_pdf(path: Path) -> str:
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(str(path))
        return "\n".join(page.get_text() for page in doc)
    except ImportError:
        return ""
