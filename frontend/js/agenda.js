/**
 * agenda.js — Painel da agenda acadêmica.
 */

import { fetchAgenda } from "./api.js";

const listEl = document.getElementById("agenda-list");
const btns = document.querySelectorAll("[data-agenda-periodo]");

export function initAgenda() {
  btns.forEach((btn) => {
    btn.addEventListener("click", () => {
      btns.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      loadAgenda(btn.dataset.agendaPeriodo);
    });
  });
  loadAgenda("hoje");
}

async function loadAgenda(periodo) {
  listEl.innerHTML = `<div class="loading-text">Carregando…</div>`;
  try {
    const events = await fetchAgenda(periodo);
    renderEvents(events, periodo);
  } catch {
    listEl.innerHTML = `<div class="error-text">Erro ao carregar agenda.</div>`;
  }
}

function renderEvents(events, periodo) {
  if (!events.length) {
    listEl.innerHTML = `<div class="empty-text">Nenhum evento para ${periodo}.</div>`;
    return;
  }
  listEl.innerHTML = events.map((e) => `
    <div class="agenda-item type-${e.type}">
      <div class="agenda-title">${e.title}</div>
      <div class="agenda-meta">
        <span>${e.date}</span>
        ${e.time ? `<span>${e.time}</span>` : ""}
        ${e.location ? `<span>${e.location}</span>` : ""}
        <span class="badge">${e.type}</span>
      </div>
    </div>
  `).join("");
}
