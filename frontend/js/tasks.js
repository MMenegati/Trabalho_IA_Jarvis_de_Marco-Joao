/**
 * tasks.js — Painel de tarefas acadêmicas.
 */

import { fetchTasks, addTask, completeTask } from "./api.js";

const listEl = document.getElementById("tasks-list");
const formEl = document.getElementById("task-form");
const inputEl = document.getElementById("task-input");
const priorityEl = document.getElementById("task-priority");
const filterBtns = document.querySelectorAll("[data-tasks-filtro]");

let currentFilter = "pendentes";

export function initTasks() {
  filterBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      filterBtns.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      currentFilter = btn.dataset.tasksFiltro;
      loadTasks();
    });
  });

  formEl.addEventListener("submit", async (e) => {
    e.preventDefault();
    const text = inputEl.value.trim();
    if (!text) return;
    await addTask(text, priorityEl.value);
    inputEl.value = "";
    loadTasks();
  });

  loadTasks();
}

async function loadTasks() {
  listEl.innerHTML = `<div class="loading-text">Carregando…</div>`;
  try {
    const tasks = await fetchTasks(currentFilter);
    renderTasks(tasks);
  } catch {
    listEl.innerHTML = `<div class="error-text">Erro ao carregar tarefas.</div>`;
  }
}

function renderTasks(tasks) {
  if (!tasks.length) {
    listEl.innerHTML = `<div class="empty-text">Nenhuma tarefa ${currentFilter}.</div>`;
    return;
  }
  listEl.innerHTML = tasks.map((t) => `
    <div class="task-item priority-${t.priority} ${t.done ? "done" : ""}">
      <div class="task-info">
        <span class="task-priority-badge">${t.priority.toUpperCase()}</span>
        <span class="task-text">${t.text}</span>
      </div>
      ${!t.done ? `<button class="complete-btn" data-id="${t.id}">✓</button>` : ""}
    </div>
  `).join("");

  listEl.querySelectorAll(".complete-btn").forEach((btn) => {
    btn.addEventListener("click", async () => {
      await completeTask(Number(btn.dataset.id));
      loadTasks();
    });
  });
}
