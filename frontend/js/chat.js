/**
 * chat.js — Renderização do painel de chat e gestão do histórico de exibição.
 */

import { sendChat } from "./api.js";
import { state } from "./app.js";

const messagesEl = document.getElementById("chat-messages");
const inputEl = document.getElementById("chat-input");
const sendBtn = document.getElementById("chat-send");
const toolsLogEl = document.getElementById("tools-log");

export function initChat() {
  sendBtn.addEventListener("click", handleSend);
  inputEl.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); handleSend(); }
  });
}

async function handleSend() {
  const message = inputEl.value.trim();
  if (!message) return;

  inputEl.value = "";
  appendMessage("user", message);
  const loadingId = appendLoading();

  try {
    const result = await sendChat(message, state.history);
    state.history = result.history;

    removeLoading(loadingId);
    appendMessage("assistant", result.reply);

    if (result.tools_called?.length > 0) {
      logTools(result.tools_called);
    }
  } catch (err) {
    removeLoading(loadingId);
    appendMessage("assistant", `Erro ao conectar ao servidor: ${err.message}`);
  }
}

function appendMessage(role, text) {
  const div = document.createElement("div");
  div.className = `message ${role}`;
  div.innerHTML = `
    <div class="message-bubble">${escapeHtml(text).replace(/\n/g, "<br>").replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")}</div>
    <span class="message-time">${new Date().toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" })}</span>
  `;
  messagesEl.appendChild(div);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

function appendLoading() {
  const id = `loading-${Date.now()}`;
  const div = document.createElement("div");
  div.className = "message assistant";
  div.id = id;
  div.innerHTML = `<div class="message-bubble loading-bubble"><span class="dot"></span><span class="dot"></span><span class="dot"></span></div>`;
  messagesEl.appendChild(div);
  messagesEl.scrollTop = messagesEl.scrollHeight;
  return id;
}

function removeLoading(id) {
  document.getElementById(id)?.remove();
}

function logTools(tools) {
  tools.forEach((t) => {
    const entry = document.createElement("div");
    entry.className = "log-entry";
    const time = new Date().toLocaleTimeString("pt-BR");
    entry.innerHTML = `<span class="log-time">${time}</span> <span class="log-tool">${t.name}</span><div class="log-result">${escapeHtml(String(t.result)).substring(0, 200)}…</div>`;
    toolsLogEl.prepend(entry);
  });
}

function escapeHtml(str) {
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}
