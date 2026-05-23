QUESTIONS = [
    {
        "id": 1,
        "question": "O que é o Teste de Turing e qual é seu objetivo em Inteligência Artificial?",
        "expected_keywords": ["turing", "inteligencia", "maquina", "humano", "conversa", "indistinguivel"],
        "type": "conceitual",
        "topic": "IA Fundamentos",
    },
    {
        "id": 2,
        "question": "Explique o conceito de Entropia de Shannon no contexto de árvores de decisão.",
        "expected_keywords": ["entropia", "shannon", "desordem", "classes", "impureza", "log", "probabilidade"],
        "type": "tecnico",
        "topic": "Árvores de Decisão",
    },
    {
        "id": 3,
        "question": "Qual a diferença entre pré-poda e pós-poda em árvores de decisão?",
        "expected_keywords": ["pre-poda", "pos-poda", "crescimento", "overfitting", "validacao", "profundidade"],
        "type": "conceitual",
        "topic": "Árvores de Decisão",
    },
    {
        "id": 4,
        "question": "O que é overfitting e como o trade-off bias-variance está relacionado a ele?",
        "expected_keywords": ["overfitting", "bias", "variance", "memorizacao", "generalizacao", "regularizacao"],
        "type": "conceitual",
        "topic": "Aprendizado de Máquina",
    },
    {
        "id": 5,
        "question": "Explique o que são embeddings e como a similaridade cosseno é usada em RAG.",
        "expected_keywords": ["embedding", "vetor", "semantica", "cosseno", "similaridade", "rag", "recuperacao"],
        "type": "tecnico",
        "topic": "Embeddings e RAG",
    },
    {
        "id": 6,
        "question": "Quais são as métricas Precision, Recall e F1-Score? Quando usar F1 em vez de acurácia?",
        "expected_keywords": ["precision", "recall", "f1", "acuracia", "desbalanceado", "falso", "positivo"],
        "type": "tecnico",
        "topic": "Avaliação de Modelos",
    },
    {
        "id": 7,
        "question": "O que é a arquitetura Transformer e qual o papel do mecanismo de Self-Attention?",
        "expected_keywords": ["transformer", "attention", "self-attention", "sequencia", "paralelismo", "bert", "gpt"],
        "type": "tecnico",
        "topic": "Redes Neurais",
    },
    {
        "id": 8,
        "question": "Explique o que é RAG (Retrieval-Augmented Generation) e descreva seu fluxo completo.",
        "expected_keywords": ["rag", "recuperacao", "chunk", "embedding", "llm", "contexto", "geracao"],
        "type": "tecnico",
        "topic": "RAG",
    },
    {
        "id": 9,
        "question": "O que é viés algorítmico e cite um exemplo real de impacto negativo em sistemas de IA?",
        "expected_keywords": ["vies", "bias", "algoritmico", "discriminacao", "grupos", "compas", "fairness"],
        "type": "conceitual",
        "topic": "Ética em IA",
    },
    {
        "id": 10,
        "question": "Explique o algoritmo A* e o que torna uma heurística admissível.",
        "expected_keywords": ["a*", "heuristica", "admissivel", "custo", "busca", "otimo", "superestime"],
        "type": "tecnico",
        "topic": "Algoritmos de Busca",
    },
]


def get_question(question_id: int) -> dict | None:
    return next((q for q in QUESTIONS if q["id"] == question_id), None)
