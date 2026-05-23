from datetime import date, timedelta
from backend.storage.database import get_connection


def _rows_to_list(rows) -> list[dict]:
    return [dict(r) for r in rows]


def get_today() -> list[dict]:
    today = date.today().isoformat()
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM events WHERE date = ? ORDER BY time", (today,)
        ).fetchall()
    return _rows_to_list(rows)


def get_tomorrow() -> list[dict]:
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM events WHERE date = ? ORDER BY time", (tomorrow,)
        ).fetchall()
    return _rows_to_list(rows)


def get_week() -> list[dict]:
    today = date.today()
    end = today + timedelta(days=7)
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM events WHERE date BETWEEN ? AND ? ORDER BY date, time",
            (today.isoformat(), end.isoformat()),
        ).fetchall()
    return _rows_to_list(rows)


def add_event(title: str, date_str: str, time_str: str = None,
              location: str = None, type_: str = "aula") -> dict:
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO events (title, date, time, location, type) VALUES (?,?,?,?,?)",
            (title, date_str, time_str, location, type_),
        )
        conn.commit()
        row = conn.execute("SELECT * FROM events WHERE id = ?", (cur.lastrowid,)).fetchone()
    return dict(row)
