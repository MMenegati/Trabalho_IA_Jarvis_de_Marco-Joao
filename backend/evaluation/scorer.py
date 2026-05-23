import re
from backend.evaluation.questions import QUESTIONS, get_question
from backend.rag import pipeline


def score_answer(question_id: int, user_answer: str) -> dict:
    """
    Avalia a resposta do usuário e retorna classificação com feedback.
    Também recupera os documentos relevantes para a questão.
    """
    question = get_question(question_id)
    if question is None:
        return {"error": f"Questão {question_id} não encontrada."}

    answer_normalized = _normalize(user_answer)
    keywords = question["expected_keywords"]
    matched, missing = _match_keywords(answer_normalized, keywords)

    score = len(matched) / len(keywords) if keywords else 0

    if score >= 0.70:
        status = "CORRETA"
        feedback = f"Excelente! Você cobriu os pontos essenciais ({len(matched)}/{len(keywords)} conceitos)."
    elif score >= 0.40:
        status = "PARCIALMENTE CORRETA"
        feedback = f"Boa tentativa! Faltaram: {', '.join(missing)}."
    else:
        status = "INCORRETA"
        feedback = f"Revise o tópico '{question['topic']}'. Conceitos-chave: {', '.join(keywords)}."

    retrieved_docs = pipeline.search(question["question"], top_k=3)

    return {
        "question_id": question_id,
        "question": question["question"],
        "topic": question["topic"],
        "status": status,
        "score": round(score, 3),
        "matched_keywords": matched,
        "missing_keywords": missing,
        "feedback": feedback,
        "retrieved_docs": [
            {"source": d["source"], "text": d["text"][:200], "score": round(d["score"], 3)}
            for d in retrieved_docs
        ],
    }


def run_full_evaluation(answers: dict[int, str]) -> dict:
    """Avalia todas as respostas e retorna sumário completo."""
    results = []
    counts = {"CORRETA": 0, "PARCIALMENTE CORRETA": 0, "INCORRETA": 0}

    for q in QUESTIONS:
        answer = answers.get(q["id"], "")
        result = score_answer(q["id"], answer)
        results.append(result)
        counts[result.get("status", "INCORRETA")] += 1

    total = len(QUESTIONS)
    return {
        "total": total,
        "summary": counts,
        "results": results,
    }


def _normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[áàãâä]", "a", text)
    text = re.sub(r"[éèêë]", "e", text)
    text = re.sub(r"[íìîï]", "i", text)
    text = re.sub(r"[óòõôö]", "o", text)
    text = re.sub(r"[úùûü]", "u", text)
    text = re.sub(r"[ç]", "c", text)
    return text


def _match_keywords(text: str, keywords: list[str]) -> tuple[list, list]:
    matched, missing = [], []
    for kw in keywords:
        kw_norm = _normalize(kw)
        if kw_norm in text or any(kw_norm[:4] in token for token in text.split()):
            matched.append(kw)
        else:
            missing.append(kw)
    return matched, missing
