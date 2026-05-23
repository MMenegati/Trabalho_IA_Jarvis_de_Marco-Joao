import sqlite3
from backend.config import DB_PATH

_CREATE_EVENTS = """
CREATE TABLE IF NOT EXISTS events (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    title    TEXT    NOT NULL,
    date     TEXT    NOT NULL,
    time     TEXT,
    location TEXT,
    type     TEXT    DEFAULT 'aula'
);
"""

_CREATE_TASKS = """
CREATE TABLE IF NOT EXISTS tasks (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    text       TEXT    NOT NULL,
    priority   TEXT    DEFAULT 'media',
    done       INTEGER DEFAULT 0,
    created_at TEXT    DEFAULT CURRENT_TIMESTAMP
);
"""

_SEED_EVENTS = """
INSERT INTO events (title, date, time, location, type) VALUES
  ('Aula de Inteligência Artificial', '2026-05-26', '08:00', 'Sala 201', 'aula'),
  ('Aula de Estruturas de Dados',     '2026-05-26', '10:00', 'Sala 105', 'aula'),
  ('Prova de Cálculo II',             '2026-05-27', '14:00', 'Sala 301', 'prova'),
  ('Aula de Redes de Computadores',   '2026-05-28', '08:00', 'Sala 202', 'aula'),
  ('Entrega Trabalho de IA',          '2026-05-30', '23:59', 'Moodle',   'trabalho'),
  ('Aula de Banco de Dados',          '2026-05-29', '10:00', 'Sala 103', 'aula'),
  ('Seminário de Pesquisa',           '2026-05-30', '14:00', 'Auditório','reuniao'),
  ('Prova de Algoritmos',             '2026-06-02', '08:00', 'Sala 201', 'prova'),
  ('Aula de Sistemas Operacionais',   '2026-06-03', '10:00', 'Sala 104', 'aula'),
  ('Defesa de TCC',                   '2026-06-05', '14:00', 'Sala 401', 'trabalho');
"""

_SEED_TASKS = """
INSERT INTO tasks (text, priority, done) VALUES
  ('Estudar árvores de decisão para prova', 'alta',  0),
  ('Ler capítulo 5 do livro de IA',         'media', 0),
  ('Implementar algoritmo K-Means',          'alta',  0),
  ('Revisar embeddings e RAG',               'media', 0),
  ('Assistir aula gravada de Redes',         'baixa', 0);
"""


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(_CREATE_EVENTS)
        conn.execute(_CREATE_TASKS)
        conn.commit()

        if conn.execute("SELECT COUNT(*) FROM events").fetchone()[0] == 0:
            conn.executescript(_SEED_EVENTS)
        if conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0] == 0:
            conn.executescript(_SEED_TASKS)
        conn.commit()
