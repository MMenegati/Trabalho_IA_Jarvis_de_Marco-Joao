from backend.rag import pipeline

_EXERCISES = {
    "árvores de decisão": {
        "enunciado": "Dado um dataset com 10 exemplos de duas classes (5 positivos, 5 negativos), calcule a entropia do conjunto raiz e o ganho de informação do atributo 'Temperatura' que divide em {Quente: 3+, 1-} e {Frio: 2+, 4-}.",
        "resposta_esperada": "Entropia raiz = 1 bit. Para Quente: H = -(3/4)log2(3/4) -(1/4)log2(1/4) ≈ 0.811. Para Frio: H = -(2/6)log2(2/6) -(4/6)log2(4/6) ≈ 0.918. Ganho = 1 - (4/10)*0.811 - (6/10)*0.918 ≈ 0.325 - 0.551 = 0.124 bits.",
    },
    "embeddings": {
        "enunciado": "Explique a diferença entre embeddings estáticos (Word2Vec) e embeddings contextuais (BERT). Por que embeddings contextuais são superiores para tarefas de compreensão de linguagem?",
        "resposta_esperada": "Word2Vec gera um único vetor fixo por palavra independente do contexto. BERT gera vetores diferentes para a mesma palavra em contextos diferentes, resolvendo polissemia. Exemplos: 'banco' (financeiro vs. assento) teriam vetores distintos em BERT.",
    },
    "redes neurais": {
        "enunciado": "Explique o problema de vanishing gradient em redes neurais profundas e como o ReLU e as conexões residuais (ResNet) ajudam a mitigá-lo.",
        "resposta_esperada": "Vanishing gradient: gradientes ficam exponencialmente pequenos ao propagar por muitas camadas com ativações Sigmoid/Tanh, impedindo o treino das camadas iniciais. ReLU tem derivada 1 para x>0, não satura. Residual connections somam a entrada ao output da camada, garantindo que o gradiente flua diretamente.",
    },
    "aprendizado de máquina": {
        "enunciado": "Um modelo tem acurácia de 99% em um dataset com 1% de positivos e 99% de negativos. Ele está realmente aprendendo? Que métricas usar?",
        "resposta_esperada": "Não necessariamente — o modelo pode estar prevendo sempre 'negativo'. Acurácia é enganosa em datasets desbalanceados. Usar Precision, Recall, F1-Score e AUC-ROC que avaliam performance na classe minoritária.",
    },
    "rag": {
        "enunciado": "Descreva o fluxo completo de um sistema RAG, desde a indexação dos documentos até a geração da resposta final. Por que a etapa de chunking é crítica?",
        "resposta_esperada": "Indexação: carregar docs → chunk → embed → armazenar vetores. Busca: embed query → cosine similarity → top-k chunks. Geração: chunks como contexto para LLM. Chunking é crítico pois chunks muito pequenos perdem contexto e chunks muito grandes reduzem precisão da recuperação.",
    },
}

_DEFAULT_EXERCISE = {
    "enunciado": "Explique o conceito de overfitting em modelos de aprendizado de máquina, suas causas e três técnicas para mitigá-lo.",
    "resposta_esperada": "Overfitting: modelo memoriza dados de treino (alto bias de treino baixo, alta variância de teste). Causas: modelo muito complexo, poucos dados, sem regularização. Mitigações: regularização L1/L2, dropout, mais dados, early stopping, validação cruzada.",
}


def gerar_exercicio(topico: str) -> str:
    topico_lower = topico.lower()
    exercicio = next(
        (v for k, v in _EXERCISES.items() if k in topico_lower),
        _DEFAULT_EXERCISE,
    )
    return (
        f"**Exercício — {topico}**\n\n"
        f"{exercicio['enunciado']}\n\n"
        f"*Tente responder antes de ver a solução esperada.*\n\n"
        f"**Resposta esperada:** {exercicio['resposta_esperada']}"
    )


def planejar_estudos(foco: str) -> str:
    from backend.storage import agenda_repo, tasks_repo

    eventos = agenda_repo.get_week()
    tarefas = tasks_repo.list_tasks("pendentes")
    chunks = pipeline.search(foco, top_k=2)

    eventos_str = "\n".join(
        f"  - {e['date']} {e.get('time','')}: {e['title']} ({e['type']})"
        for e in eventos
    ) or "  Nenhum evento esta semana."

    tarefas_str = "\n".join(
        f"  - [{t['priority'].upper()}] {t['text']}"
        for t in tarefas
    ) or "  Nenhuma tarefa pendente."

    material_str = "\n".join(
        f"  - {c['source']}: {c['text'][:120]}…"
        for c in chunks
    ) or "  Nenhum material encontrado."

    return (
        f"**Plano de estudos — Foco: {foco}**\n\n"
        f"Agenda da semana:\n{eventos_str}\n\n"
        f"Tarefas pendentes:\n{tarefas_str}\n\n"
        f"Materiais relevantes encontrados:\n{material_str}"
    )
