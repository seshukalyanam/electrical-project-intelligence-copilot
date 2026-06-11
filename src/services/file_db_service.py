from __future__ import annotations

from pathlib import Path
from typing import Any

from src.utils.config import LOCAL_DB_DIR, LOCAL_DB_SUBFOLDERS
from src.utils.helpers import utc_stamp, write_json


def ensure_local_db() -> None:
    for folder in LOCAL_DB_SUBFOLDERS:
        (LOCAL_DB_DIR / folder).mkdir(parents=True, exist_ok=True)


def save_chat(project_id: str, question: str, answer: str, sources: list[dict[str, Any]]) -> Path:
    ensure_local_db()
    path = LOCAL_DB_DIR / "chat_logs" / f"{project_id}_{utc_stamp()}.json"
    write_json(path, {"project_id": project_id, "question": question, "answer": answer, "sources": sources})
    return path


def save_voice_transcript(project_id: str, transcript: str, answer: str) -> Path:
    ensure_local_db()
    path = LOCAL_DB_DIR / "voice_transcripts" / f"{project_id}_{utc_stamp()}.json"
    write_json(path, {"project_id": project_id, "transcript": transcript, "answer": answer})
    return path


def save_ingestion_log(payload: dict[str, Any]) -> Path:
    ensure_local_db()
    path = LOCAL_DB_DIR / "ingestion_logs" / f"ingestion_{utc_stamp()}.json"
    write_json(path, payload)
    return path
