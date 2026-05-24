"""
JARVIS Acadêmico — FastAPI entrypoint
Serve a API REST e os arquivos estáticos do frontend.
"""
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from backend.storage.database import init_db
from backend.rag import pipeline as rag_pipeline
from backend.llm import client as llm_client
from backend.storage import agenda_repo, tasks_repo
from backend.evaluation.questions import QUESTIONS
from backend.evaluation.scorer import score_answer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    rag_pipeline.build_index()
    yield


app = FastAPI(title="JARVIS Acadêmico", version="2.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

FRONTEND_DIR = Path(__file__).parent.parent / "frontend"


# ── Chat ─────────────────────────────────────────────────────────────────────

class ChatRequest(BaseModel):
    message: str
    history: list[dict] = []


@app.post("/api/chat")
async def chat(req: ChatRequest):
    import traceback
    try:
        result = llm_client.chat(req.message, req.history)
        return result
    except Exception as exc:
        logging.getLogger("jarvis.api").error("Erro no chat: %s\n%s", exc, traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(exc))


# ── Agenda ───────────────────────────────────────────────────────────────────

@app.get("/api/agenda/{periodo}")
async def get_agenda(periodo: str):
    if periodo == "hoje":
        return agenda_repo.get_today()
    elif periodo == "amanha":
        return agenda_repo.get_tomorrow()
    elif periodo == "semana":
        return agenda_repo.get_week()
    raise HTTPException(status_code=400, detail="Período inválido.")


# ── Tasks ─────────────────────────────────────────────────────────────────────

class TaskRequest(BaseModel):
    text: str
    priority: str = "media"


@app.get("/api/tasks")
async def list_tasks(filtro: str = "pendentes"):
    return tasks_repo.list_tasks(filtro)


@app.post("/api/tasks")
async def add_task(req: TaskRequest):
    return tasks_repo.add_task(req.text, req.priority)


@app.patch("/api/tasks/{task_id}/complete")
async def complete_task(task_id: int):
    task = tasks_repo.complete_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada.")
    return task


# ── RAG ──────────────────────────────────────────────────────────────────────

class RagRequest(BaseModel):
    query: str
    top_k: int = 3


@app.post("/api/rag/search")
async def rag_search(req: RagRequest):
    results = rag_pipeline.search(req.query, req.top_k)
    return results


# ── Avaliação ─────────────────────────────────────────────────────────────────

@app.get("/api/evaluation/questions")
async def get_questions():
    return QUESTIONS


class ScoreRequest(BaseModel):
    question_id: int
    answer: str


@app.post("/api/evaluation/score")
async def score(req: ScoreRequest):
    result = score_answer(req.question_id, req.answer)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


# ── Frontend estático ─────────────────────────────────────────────────────────

app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


@app.get("/")
async def serve_index():
    return FileResponse(str(FRONTEND_DIR / "index.html"))


@app.get("/{path:path}")
async def serve_static(path: str):
    file_path = FRONTEND_DIR / path
    if file_path.exists() and file_path.is_file():
        return FileResponse(str(file_path))
    return FileResponse(str(FRONTEND_DIR / "index.html"))
