from backend.storage.database import get_connection


def _rows_to_list(rows) -> list[dict]:
    return [dict(r) for r in rows]


def list_tasks(filtro: str = "pendentes") -> list[dict]:
    done_flag = 0 if filtro == "pendentes" else 1
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM tasks WHERE done = ? ORDER BY priority DESC, id",
            (done_flag,),
        ).fetchall()
    return _rows_to_list(rows)


def add_task(text: str, priority: str = "media") -> dict:
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO tasks (text, priority) VALUES (?, ?)", (text, priority)
        )
        conn.commit()
        row = conn.execute("SELECT * FROM tasks WHERE id = ?", (cur.lastrowid,)).fetchone()
    return dict(row)


def complete_task(task_id: int) -> dict | None:
    with get_connection() as conn:
        conn.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
        conn.commit()
        row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    return dict(row) if row else None


def get_all_tasks() -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM tasks ORDER BY done, priority DESC").fetchall()
    return _rows_to_list(rows)
