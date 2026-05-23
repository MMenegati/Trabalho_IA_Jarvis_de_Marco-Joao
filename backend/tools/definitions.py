"""
Schemas JSON das ferramentas enviados à Gemma.
A LLM lê estas definições e decide quais chamar — não há lógica fixa de despacho.
"""

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "consultar_agenda",
            "description": "Consulta os eventos da agenda acadêmica do estudante para um período específico.",
            "parameters": {
                "type": "object",
                "properties": {
                    "periodo": {
                        "type": "string",
                        "enum": ["hoje", "amanha", "semana"],
                        "description": "Período a consultar: 'hoje', 'amanha' ou 'semana' (próximos 7 dias).",
                    }
                },
                "required": ["periodo"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "listar_tarefas",
            "description": "Lista as tarefas acadêmicas do estudante, filtrando por status.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filtro": {
                        "type": "string",
                        "enum": ["pendentes", "concluidas"],
                        "description": "Filtrar por 'pendentes' ou 'concluidas'.",
                    }
                },
                "required": ["filtro"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "adicionar_tarefa",
            "description": "Adiciona uma nova tarefa acadêmica à lista do estudante.",
            "parameters": {
                "type": "object",
                "properties": {
                    "texto": {
                        "type": "string",
                        "description": "Descrição da tarefa a adicionar.",
                    },
                    "prioridade": {
                        "type": "string",
                        "enum": ["alta", "media", "baixa"],
                        "description": "Prioridade da tarefa.",
                    },
                },
                "required": ["texto", "prioridade"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "concluir_tarefa",
            "description": "Marca uma tarefa como concluída pelo seu ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "ID numérico da tarefa a concluir.",
                    }
                },
                "required": ["task_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "buscar_material_rag",
            "description": "Busca trechos relevantes na base de conhecimento acadêmica sobre um tópico.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Pergunta ou tópico a buscar nos materiais acadêmicos.",
                    }
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "gerar_exercicio",
            "description": "Gera um exercício ou questão de prática sobre um tópico acadêmico.",
            "parameters": {
                "type": "object",
                "properties": {
                    "topico": {
                        "type": "string",
                        "description": "Tópico para gerar o exercício (ex: 'árvores de decisão', 'embeddings', 'redes neurais').",
                    }
                },
                "required": ["topico"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "planejar_estudos",
            "description": "Gera um plano de estudos personalizado combinando agenda, tarefas pendentes e materiais disponíveis.",
            "parameters": {
                "type": "object",
                "properties": {
                    "foco": {
                        "type": "string",
                        "description": "Objetivo do plano (ex: 'prova de IA', 'entrega de trabalho', 'revisão geral').",
                    }
                },
                "required": ["foco"],
            },
        },
    },
]
