/**
 * api.js — Único módulo que faz chamadas fetch ao backend.
 * Nenhum outro módulo acessa a rede diretamente.
 */

const BASE = "";

export async function sendChat(message, history) {
  const res = await fetch(`${BASE}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, history }),
  });
  if (!res.ok) throw new Error(`Chat error: ${res.status}`);
  return res.json();
}

export async function fetchAgenda(periodo) {
  const res = await fetch(`${BASE}/api/agenda/${periodo}`);
  if (!res.ok) throw new Error(`Agenda error: ${res.status}`);
  return res.json();
}

export async function fetchTasks(filtro = "pendentes") {
  const res = await fetch(`${BASE}/api/tasks?filtro=${filtro}`);
  if (!res.ok) throw new Error(`Tasks error: ${res.status}`);
  return res.json();
}

export async function addTask(text, priority = "media") {
  const res = await fetch(`${BASE}/api/tasks`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, priority }),
  });
  if (!res.ok) throw new Error(`Add task error: ${res.status}`);
  return res.json();
}

export async function completeTask(taskId) {
  const res = await fetch(`${BASE}/api/tasks/${taskId}/complete`, { method: "PATCH" });
  if (!res.ok) throw new Error(`Complete task error: ${res.status}`);
  return res.json();
}

export async function ragSearch(query, topK = 3) {
  const res = await fetch(`${BASE}/api/rag/search`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, top_k: topK }),
  });
  if (!res.ok) throw new Error(`RAG error: ${res.status}`);
  return res.json();
}

export async function fetchQuestions() {
  const res = await fetch(`${BASE}/api/evaluation/questions`);
  if (!res.ok) throw new Error(`Questions error: ${res.status}`);
  return res.json();
}

export async function scoreAnswer(questionId, answer) {
  const res = await fetch(`${BASE}/api/evaluation/score`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question_id: questionId, answer }),
  });
  if (!res.ok) throw new Error(`Score error: ${res.status}`);
  return res.json();
}
