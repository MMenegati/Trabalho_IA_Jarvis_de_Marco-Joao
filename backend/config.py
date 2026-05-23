from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

API_BASE_URL = "https://llm.liaufms.org/v1/gemma-3-12b-it"
API_KEY = "Cxt2ftLF7d3mHS2JdiFqB-eSDAQeZvFATPXPs02lV9A"
MODEL = "google/gemma-3-12b-it"

DATA_DIR = BASE_DIR / "data" / "raw"
CHUNKS_CACHE = BASE_DIR / "data" / "chunks.json"
DB_PATH = BASE_DIR / "storage" / "jarvis.db"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
CHUNK_SIZE = 200
CHUNK_OVERLAP = 50
TOP_K = 3

LLM_TIMEOUT = 60
LLM_MAX_RETRIES = 3
LLM_MAX_TOKENS = 1024
LLM_TEMPERATURE = 0.7
HISTORY_WINDOW = 6
