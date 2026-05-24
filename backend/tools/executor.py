"""
Recebe tool_calls[] retornados pela Gemma e despacha para as implementações reais.
Registra log de cada execução.
"""
import json
import logging
from datetime import datetime

# Mapeamento de aliases que a LLM costuma inventar → nome correto do parâmetro
_ARG_ALIASES: dict[str, dict[str, str]] = {
    "listar_tarefas": {
        "status": "filtro",
        "tipo": "filtro",
        "filter": "filtro",
    },
    "adicionar_tarefa": {
        "tarefa": "texto",
        "task": "texto",
        "descricao": "texto",
        "description": "texto",
        "text": "texto",
        "titulo": "texto",
        "priority": "prioridade",
    },
    "consultar_agenda": {
        "period": "periodo",
        "período": "periodo",
    },
}

from backend.tools.agenda import consultar_agenda
from backend.tools.tasks import listar_tarefas, adicionar_tarefa, concluir_tarefa
from backend.tools.rag_tool import buscar_material_rag
from backend.tools.learning import gerar_exercicio, planejar_estudos

logger = logging.getLogger("jarvis.tools")

_REGISTRY = {
    "consultar_agenda":   consultar_agenda,
    "listar_tarefas":     listar_tarefas,
    "adicionar_tarefa":   adicionar_tarefa,
    "concluir_tarefa":    concluir_tarefa,
    "buscar_material_rag": buscar_material_rag,
    "gerar_exercicio":    gerar_exercicio,
    "planejar_estudos":   planejar_estudos,
}


def execute(tool_calls) -> list[dict]:
    """
    Executa todas as tool_calls da LLM.
    Retorna lista de {tool_call_id, name, result} para reenvio à LLM.
    """
    results = []
    for call in tool_calls:
        name = call.function.name
        try:
            args = json.loads(call.function.arguments)
        except json.JSONDecodeError:
            args = {}

        # Normaliza aliases de parâmetros que a LLM pode inventar
        aliases = _ARG_ALIASES.get(name, {})
        args = {aliases.get(k, k): v for k, v in args.items()}

        fn = _REGISTRY.get(name)
        if fn is None:
            output = f"Ferramenta '{name}' não encontrada."
            status = "error"
        else:
            try:
                output = fn(**args)
                status = "ok"
            except Exception as exc:
                output = f"Erro ao executar '{name}': {exc}"
                status = "error"

        logger.info(
            "tool_call | time=%s | tool=%s | args=%s | status=%s | output_len=%d",
            datetime.now().isoformat(timespec="seconds"),
            name,
            json.dumps(args, ensure_ascii=False),
            status,
            len(str(output)),
        )

        results.append({
            "tool_call_id": call.id,
            "name": name,
            "result": output,
        })

    return results
