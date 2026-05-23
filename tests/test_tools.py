"""Testes das ferramentas: agenda, tasks, definitions."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.storage.database import init_db
from backend.storage import agenda_repo, tasks_repo
from backend.tools.definitions import TOOL_DEFINITIONS

# Garante que o banco existe antes dos testes
init_db()


def test_tool_definitions_count():
    assert len(TOOL_DEFINITIONS) >= 5, f"Esperado >= 5 ferramentas, encontrado {len(TOOL_DEFINITIONS)}"


def test_tool_definitions_schema():
    required_fields = {"type", "function"}
    for tool in TOOL_DEFINITIONS:
        assert required_fields.issubset(tool.keys()), f"Tool sem campos obrigatórios: {tool}"
        fn = tool["function"]
        assert "name" in fn and "description" in fn and "parameters" in fn


def test_tool_names_match_registry():
    from backend.tools.executor import _REGISTRY
    defined_names = {t["function"]["name"] for t in TOOL_DEFINITIONS}
    registry_names = set(_REGISTRY.keys())
    missing = defined_names - registry_names
    assert not missing, f"Ferramentas definidas mas não no registry: {missing}"


def test_agenda_get_week_returns_list():
    events = agenda_repo.get_week()
    assert isinstance(events, list)


def test_agenda_events_have_required_fields():
    events = agenda_repo.get_week()
    for e in events:
        assert "id" in e and "title" in e and "date" in e


def test_tasks_list_returns_list():
    tasks = tasks_repo.list_tasks("pendentes")
    assert isinstance(tasks, list)


def test_tasks_add_and_complete():
    task = tasks_repo.add_task("Tarefa de teste automatizado", "media")
    assert task["text"] == "Tarefa de teste automatizado"
    assert task["done"] == 0

    completed = tasks_repo.complete_task(task["id"])
    assert completed["done"] == 1


def test_complete_nonexistent_task_returns_none():
    result = tasks_repo.complete_task(999999)
    assert result is None


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try:
                fn()
                print(f"  PASS  {name}")
            except AssertionError as e:
                print(f"  FAIL  {name}: {e}")
