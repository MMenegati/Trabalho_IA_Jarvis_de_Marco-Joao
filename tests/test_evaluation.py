"""Testes do módulo de avaliação."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.evaluation.questions import QUESTIONS, get_question
from backend.evaluation.scorer import score_answer, _normalize, _match_keywords


def test_questions_count():
    assert len(QUESTIONS) == 10, f"Esperado 10 questões, encontrado {len(QUESTIONS)}"


def test_questions_have_required_fields():
    for q in QUESTIONS:
        for field in ("id", "question", "expected_keywords", "type", "topic"):
            assert field in q, f"Questão {q.get('id')} sem campo '{field}'"


def test_get_question_found():
    q = get_question(1)
    assert q is not None and q["id"] == 1


def test_get_question_not_found():
    assert get_question(99) is None


def test_normalize_removes_accents():
    assert _normalize("áéíóúç") == "aeiouc"


def test_match_keywords_full_match():
    matched, missing = _match_keywords("entropia ganho arvore decisao", ["entropia", "ganho", "arvore"])
    assert len(matched) == 3 and len(missing) == 0


def test_match_keywords_no_match():
    matched, missing = _match_keywords("nada relevante aqui", ["entropia", "ganho"])
    assert len(matched) == 0 and len(missing) == 2


def test_score_correta():
    # Resposta com todos os keywords da questão 2 (entropia)
    full_answer = "entropia shannon desordem classes impureza log probabilidade ganho informacao"
    result = score_answer(2, full_answer)
    assert result["status"] == "CORRETA"


def test_score_incorreta():
    result = score_answer(2, "não sei nada sobre isso mesmo")
    assert result["status"] == "INCORRETA"


def test_score_result_has_retrieved_docs():
    result = score_answer(1, "turing inteligencia maquina conversa")
    assert "retrieved_docs" in result
    assert isinstance(result["retrieved_docs"], list)


def test_score_invalid_question():
    result = score_answer(99, "resposta qualquer")
    assert "error" in result


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try:
                fn()
                print(f"  PASS  {name}")
            except AssertionError as e:
                print(f"  FAIL  {name}: {e}")
            except Exception as e:
                print(f"  ERROR {name}: {e}")
