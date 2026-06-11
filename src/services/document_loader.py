from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import fitz

from src.utils.config import DATA_DIR, PROJECTS


@dataclass
class DocumentChunk:
    text: str
    metadata: dict


def document_type(path: Path) -> str:
    parts = [p.lower() for p in path.parts]
    for candidate in ["drawings", "specs", "schedules", "rfi", "change_orders", "materials", "safety", "estimates", "summaries"]:
        if candidate in parts:
            return candidate
    return path.suffix.lstrip(".") or "unknown"


def _read_pdf(path: Path) -> Iterable[tuple[str, int]]:
    doc = fitz.open(path)
    for idx, page in enumerate(doc, start=1):
        text = page.get_text("text").strip()
        if text:
            yield text, idx


def _read_csv(path: Path) -> str:
    rows = list(csv.DictReader(path.open("r", encoding="utf-8", newline="")))
    return "\n".join(json.dumps(row, ensure_ascii=False) for row in rows)


def _read_file(path: Path) -> Iterable[tuple[str, int | None]]:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        yield from _read_pdf(path)
    elif suffix == ".csv":
        yield _read_csv(path), None
    elif suffix == ".json":
        yield json.dumps(json.loads(path.read_text(encoding="utf-8")), indent=2), None
    elif suffix in {".txt", ".md"}:
        yield path.read_text(encoding="utf-8"), None


def chunk_text(text: str, size: int = 900, overlap: int = 160) -> list[str]:
    text = " ".join(text.split())
    if len(text) <= size:
        return [text] if text else []
    chunks: list[str] = []
    start = 0
    while start < len(text):
        chunks.append(text[start : start + size])
        start += max(1, size - overlap)
    return chunks


def load_project_documents(project_id: str) -> list[DocumentChunk]:
    project_dir = DATA_DIR / project_id
    chunks: list[DocumentChunk] = []
    project_name = PROJECTS[project_id]
    for path in sorted(project_dir.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".pdf", ".txt", ".md", ".csv", ".json"}:
            continue
        for raw_text, page_number in _read_file(path):
            for section_idx, chunk in enumerate(chunk_text(raw_text), start=1):
                chunks.append(
                    DocumentChunk(
                        text=chunk,
                        metadata={
                            "project_id": project_id,
                            "project_name": project_name,
                            "document_type": document_type(path),
                            "source_file": path.name,
                            "page_number": page_number,
                            "section": section_idx,
                            "folder_path": str(path.parent),
                            "path": str(path),
                        },
                    )
                )
    return chunks


def load_all_documents() -> list[DocumentChunk]:
    all_chunks: list[DocumentChunk] = []
    for project_id in PROJECTS:
        if (DATA_DIR / project_id).exists():
            all_chunks.extend(load_project_documents(project_id))
    return all_chunks
