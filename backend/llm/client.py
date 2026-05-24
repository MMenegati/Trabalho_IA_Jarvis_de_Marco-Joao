"""
Cliente LLM — tool calling via prompt estruturado (JSON).
O servidor llm.liaufms.org não tem --enable-auto-tool-choice,
então usamos o modo prompt: a LLM retorna JSON com as ferramentas
que quer chamar, o executor as executa e uma 2ª chamada gera a resposta final.
A LLM ainda decide quais ferramentas chamar — não é lógica fixa.
"""
import json
import logging
import time

from openai import OpenAI, APIError, RateLimitError

from backend.config import (API_BASE_URL, API_KEY, MODEL, LLM_TIMEOUT,
                             LLM_MAX_RETRIES, LLM_MAX_TOKENS, LLM_TEMPERATURE,
                             HISTORY_WINDOW)
from backend.llm.prompts import SYSTEM_PROMPT, TOOL_FALLBACK_PROMPT
from backend.tools.definitions import TOOL_DEFINITIONS
from backend.tools import executor

logger = logging.getLogger("jarvis.llm")

_client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY, timeout=LLM_TIMEOUT)

def _format_tool_desc(t: dict) -> str:
    """Formata nome + descrição + parâmetros para o prompt de roteamento."""
    fn = t["function"]
    props = fn.get("parameters", {}).get("properties", {})
    required = fn.get("parameters", {}).get("required", [])
    lines = [f"- {fn['name']}: {fn['description']}"]
    if props:
        lines.append("  Parâmetros (use EXATAMENTE estes nomes):")
        for p_name, p_info in props.items():
            req = " [obrigatório]" if p_name in required else " [opcional]"
            enum = p_info.get("enum")
            enum_str = f" — valores: {' | '.join(enum)}" if enum else ""
            lines.append(f"    - {p_name}{req}{enum_str}: {p_info.get('description', '')}")
    return "\n".join(lines)


_TOOL_NAMES_DESC = "\n".join(_format_tool_desc(t) for t in TOOL_DEFINITIONS)


def chat(message: str, history: list[dict]) -> dict:
    """
    Fluxo:
      1. Pede à LLM que decida quais ferramentas chamar (resposta JSON)
      2. Executa as ferramentas escolhidas
      3. Envia resultados + mensagem original para a LLM gerar resposta final
    """
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages += history[-HISTORY_WINDOW:]
    messages.append({"role": "user", "content": message})

    # ── Etapa 1: LLM decide as ferramentas ───────────────────────────────────
    tools_called = []
    tool_context = ""

    tool_calls = _decide_tools(message)

    if tool_calls:
        # ── Etapa 2: executa as ferramentas ──────────────────────────────────
        for call in tool_calls:
            name = call.get("name", "")
            args = call.get("args", {})
            fake_call = _make_fake_call(name, args)
            if fake_call is None:
                continue
            results = executor.execute([fake_call])
            for r in results:
                tools_called.append({"name": r["name"], "result": r["result"]})
                tool_context += f"\n--- {r['name']} ---\n{r['result']}\n"

        # ── Etapa 3: 2ª chamada com resultados como contexto ─────────────────
        messages[-1] = {
            "role": "user",
            "content": message + "\n\n[Resultados das ferramentas:]\n" + tool_context,
        }

    response = _call_with_retry(messages)
    reply = response.choices[0].message.content or ""

    updated_history = history + [
        {"role": "user", "content": message},
        {"role": "assistant", "content": reply},
    ]
    return {"reply": reply, "tools_called": tools_called, "history": updated_history}


def _decide_tools(message: str) -> list[dict]:
    """Chama a LLM com um prompt estruturado para decidir quais ferramentas usar."""
    detection_prompt = TOOL_FALLBACK_PROMPT.format(
        tools=_TOOL_NAMES_DESC,
        message=message,
    )
    detection_msgs = [
        {"role": "system", "content": "Você é um roteador de ferramentas. Responda APENAS com JSON válido, sem explicações."},
        {"role": "user", "content": detection_prompt},
    ]
    try:
        resp = _call_with_retry(detection_msgs)
        raw = (resp.choices[0].message.content or "{}").strip()
        calls = _extract_tool_calls(raw)
        if calls:
            logger.info("LLM decidiu usar ferramentas: %s", [c.get("name") for c in calls])
        return calls
    except Exception as exc:
        logger.warning("Falha ao obter decisão de ferramentas da LLM: %s", exc)
        return []


def _extract_tool_calls(raw: str) -> list[dict]:
    """
    Extrai tool calls do texto da LLM mesmo se o JSON vier malformado.
    Tenta várias estratégias em ordem.
    """
    import re

    # Estratégia 1: JSON direto
    try:
        return json.loads(raw).get("tools", [])
    except json.JSONDecodeError:
        pass

    # Estratégia 2: extrair bloco de código markdown
    code_match = re.search(r"```(?:json)?\s*([\s\S]+?)```", raw)
    if code_match:
        try:
            return json.loads(code_match.group(1).strip()).get("tools", [])
        except json.JSONDecodeError:
            pass

    # Estratégia 3: encontrar o primeiro {...} no texto
    brace_match = re.search(r"\{[\s\S]+\}", raw)
    if brace_match:
        try:
            return json.loads(brace_match.group()).get("tools", [])
        except json.JSONDecodeError:
            pass

    # Estratégia 4: a LLM disse que não precisa de ferramentas
    if any(kw in raw.lower() for kw in ("nenhuma", "não precisa", "no tools", '"tools": []')):
        return []

    logger.warning("Não foi possível extrair JSON de: %.200s", raw)
    return []


def _make_fake_call(name: str, args: dict):
    """Cria objeto compatível com executor.execute() a partir de name+args."""
    valid_names = {t["function"]["name"] for t in TOOL_DEFINITIONS}
    if name not in valid_names:
        logger.warning("Ferramenta desconhecida ignorada: %s", name)
        return None

    class _FakeFunction:
        def __init__(self, n, a):
            self.name = n
            self.arguments = json.dumps(a, ensure_ascii=False)

    class _FakeCall:
        def __init__(self, n, a):
            self.id = f"prompt_{n}"
            self.function = _FakeFunction(n, a)

    return _FakeCall(name, args)


def _call_with_retry(messages: list[dict], **extra_kwargs):
    kwargs = {
        "model": MODEL,
        "messages": messages,
        "max_tokens": LLM_MAX_TOKENS,
        "temperature": LLM_TEMPERATURE,
        **extra_kwargs,
    }
    for attempt in range(LLM_MAX_RETRIES):
        try:
            return _client.chat.completions.create(**kwargs)
        except RateLimitError:
            wait = 2 ** attempt
            logger.warning("Rate limit. Aguardando %ds…", wait)
            time.sleep(wait)
        except APIError as exc:
            status = getattr(exc, "status_code", 0)
            if status == 400:
                raise  # erro de requisição — não adianta tentar de novo
            if attempt == LLM_MAX_RETRIES - 1:
                raise
            wait = 2 ** attempt
            logger.warning("APIError (tentativa %d/%d): %s. Aguardando %ds…",
                           attempt + 1, LLM_MAX_RETRIES, exc, wait)
            time.sleep(wait)

    raise RuntimeError("Número máximo de tentativas atingido.")
