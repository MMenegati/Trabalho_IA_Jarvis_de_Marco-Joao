/**
 * app.js — Estado global e inicialização dos módulos.
 * Importado como <script type="module"> no index.html.
 */

import { initChat } from "./chat.js";
import { initAgenda } from "./agenda.js";
import { initTasks } from "./tasks.js";

export const state = {
  history: [],         // histórico de mensagens para a LLM
  activePanel: "chat",
};

function initNav() {
  const navBtns = document.querySelectorAll("[data-panel]");
  navBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      navBtns.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");

      document.querySelectorAll(".panel").forEach((p) => p.classList.remove("active"));
      const target = document.getElementById(`panel-${btn.dataset.panel}`);
      if (target) target.classList.add("active");

      state.activePanel = btn.dataset.panel;
    });
  });
}

document.addEventListener("DOMContentLoaded", () => {
  initNav();
  initChat();
  initAgenda();
  initTasks();
});
