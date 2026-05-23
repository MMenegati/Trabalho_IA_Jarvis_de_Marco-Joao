from backend.storage import tasks_repo


def listar_tarefas(filtro: str = "pendentes") -> str:
    tasks = tasks_repo.list_tasks(filtro)
    if not tasks:
        return f"Nenhuma tarefa {filtro}."
    label = "Pendentes" if filtro == "pendentes" else "Concluídas"
    lines = [f"Tarefas {label}:"]
    for t in tasks:
        status = "✓" if t["done"] else "○"
        lines.append(f"  [{t['id']}] {status} [{t['priority'].upper()}] {t['text']}")
    return "\n".join(lines)


def adicionar_tarefa(texto: str, prioridade: str = "media") -> str:
    task = tasks_repo.add_task(texto, prioridade)
    return f"Tarefa adicionada com ID {task['id']}: '{task['text']}' (prioridade: {task['priority']})"


def concluir_tarefa(task_id: int) -> str:
    task = tasks_repo.complete_task(task_id)
    if task is None:
        return f"Tarefa com ID {task_id} não encontrada."
    return f"Tarefa [{task_id}] marcada como concluída: '{task['text']}'"
