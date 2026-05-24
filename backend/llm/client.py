"""
Cliente LLM com ciclo completo de tool calling:
1ª chamada → Gemma decide quais tools chamar
executor executa as tools
2ª chamada → Gemma gera resposta final com os resultados
"""
import logging
import time

from openai import OpenAI, APIError, RateLimitError

from backend.config import API_BASE_URL, API_KEY, MODEL, LLM_TIMEOUT, LLM_MAX_RETRIES, LLM_MAX_TOKENS, LLM_TEMPERATURE, HISTORY_WINDOW
from backend.llm.prompts import SYSTEM_PROMPT
from backend.tools.definitions import TOOL_DEFINITIONS
from backend.tools import executor

logger = logging.getLogger("jarvis.llm")

_client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY, timeout=LLM_TIMEOUT)


def chat(message: str, history: list[dict]) -> dict:
    """
    Executa o ciclo completo: mensagem → tool calling → resposta final.

    Retorna:
        {
            "reply": str,
            "tools_called": [{"name": str, "args": dict, "result": str}],
            "history": list[dict],   # histórico atualizado
        }
    """
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages += history[-HISTORY_WINDOW:]
    messages.append({"role": "user", "content": message})

    # ── 1ª chamada: Gemma decide quais ferramentas usar ───────────────────────
    response = _call_with_retry(messages, tools=TOOL_DEFINITIONS)
    assistant_msg = response.choices[0].message
    tools_called = []

    if assistant_msg.tool_calls:
        # ── Executa as ferramentas escolhidas pela LLM ────────────────────────
        tool_results = executor.execute(assistant_msg.tool_calls)
        tools_called = [
            {"name": r["name"], "result": r["result"]}
            for r in tool_results
        ]

        # ── Monta mensagens com resultados para 2ª chamada ───────────────────
        messages.append(assistant_msg)
        for r in tool_results:
            messages.append({
                "role": "tool",
                "tool_call_id": r["tool_call_id"],
                "content": r["result"],
            })

        # ── 2ª chamada: Gemma gera resposta final ─────────────────────────────
        response = _call_with_retry(messages)
        assistant_msg = response.choices[0].message

    reply = assistant_msg.content or ""

    updated_history = history + [
        {"role": "user", "content": message},
        {"role": "assistant", "content": reply},
    ]

    return {"reply": reply, "tools_called": tools_called, "history": updated_history}


def _call_with_retry(messages: list[dict], tools=None):
    """Chama a API com retry e backoff exponencial."""
    kwargs = {
        "model": MODEL,
        "messages": messages,
        "max_tokens": LLM_MAX_TOKENS,
        "temperature": LLM_TEMPERATURE,
    }
    if tools:
        kwargs["tools"] = tools
        kwargs["tool_choice"] = "auto"

    for attempt in range(LLM_MAX_RETRIES):
        try:
            return _client.chat.completions.create(**kwargs)
        except RateLimitError:
            wait = 2 ** attempt
            logger.warning("Rate limit atingido. Aguardando %ds…", wait)
            time.sleep(wait)
        except APIError as exc:
            if attempt == LLM_MAX_RETRIES - 1:
                raise
            wait = 2 ** attempt
            logger.warning("APIError (tentativa %d/%d): %s. Aguardando %ds…",
                           attempt + 1, LLM_MAX_RETRIES, exc, wait)
            time.sleep(wait)

    raise RuntimeError("Número máximo de tentativas atingido.")
