from pathlib import Path
import os

ROOT_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT_DIR / "data"
LOCAL_DB_DIR = ROOT_DIR / "local_db"
VECTOR_STORE_DIR = ROOT_DIR / "local_vector_store"
PROJECTS = {
    "school": "School",
    "hospital": "Hospital",
    "food_mart": "Food Mart",
}
PROJECT_ALIASES = {
    "School": "school",
    "Hospital": "hospital",
    "Food Mart": "food_mart",
}
MODEL_OPTIONS = ["qwen2.5", "llama3.1", "llama3.2", "mistral"]
DEFAULT_MODEL = os.getenv("DEFAULT_OLLAMA_MODEL", "qwen2.5")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_TIMEOUT_SECONDS = int(os.getenv("OLLAMA_TIMEOUT_SECONDS", "600"))
USE_SENTENCE_TRANSFORMERS = os.getenv("USE_SENTENCE_TRANSFORMERS", "false").lower() == "true"

DATA_SUBFOLDERS = [
    "drawings",
    "specs",
    "schedules",
    "rfi",
    "change_orders",
    "materials",
    "safety",
    "estimates",
    "summaries",
]

LOCAL_DB_SUBFOLDERS = [
    "chat_logs",
    "estimates",
    "project_metadata",
    "ingestion_logs",
    "voice_transcripts",
    "evaluation_results",
]
