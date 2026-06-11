from __future__ import annotations

import json
import math
import re
from pathlib import Path
from typing import Any

import numpy as np

from src.services.document_loader import DocumentChunk, load_all_documents, load_project_documents
from src.services.embedding_service import EmbeddingService
from src.services.file_db_service import save_ingestion_log
from src.utils.config import VECTOR_STORE_DIR
from src.utils.helpers import write_json


class LocalVectorStore:
    def __init__(self, store_dir: Path = VECTOR_STORE_DIR):
        self.store_dir = store_dir
        self.embedding_service = EmbeddingService()
        self.index_path = self.store_dir / "vectors.npy"
        self.docs_path = self.store_dir / "documents.json"

    def build(self, project_id: str | None = None) -> dict[str, Any]:
        self.store_dir.mkdir(parents=True, exist_ok=True)
        chunks = load_project_documents(project_id) if project_id else load_all_documents()
        texts = [chunk.text for chunk in chunks]
        vectors = self.embedding_service.embed(texts) if texts else np.zeros((0, 384), dtype=np.float32)
        np.save(self.index_path, vectors)
        write_json(self.docs_path, [{"text": c.text, "metadata": c.metadata} for c in chunks])
        payload = {"chunks": len(chunks), "projects": sorted({c.metadata["project_id"] for c in chunks})}
        save_ingestion_log(payload)
        return payload

    def _load(self) -> tuple[np.ndarray, list[dict[str, Any]]]:
        if not self.index_path.exists() or not self.docs_path.exists():
            self.build()
        vectors = np.load(self.index_path)
        docs = json.loads(self.docs_path.read_text(encoding="utf-8"))
        return vectors, docs

    def search(self, query: str, project_id: str, top_k: int = 6) -> list[dict[str, Any]]:
        vectors, docs = self._load()
        if len(docs) == 0:
            return []
        query_vec = self.embedding_service.embed([query])[0]
        q_tokens = set(re.findall(r"[a-z0-9]+", query.lower()))
        if {"rfi", "rfis", "unresolved", "open"} & q_tokens:
            q_tokens.update({"rfi", "rfis", "open", "unresolved", "status", "question"})
        if {"change", "order", "revision", "impact"} & q_tokens:
            q_tokens.update({"change", "order", "revision", "impact", "cost", "schedule"})
        results = []
        for idx, doc in enumerate(docs):
            meta = doc["metadata"]
            if meta.get("project_id") != project_id:
                continue
            text = doc["text"]
            vector_score = float(np.dot(vectors[idx], query_vec)) if idx < len(vectors) else 0.0
            d_tokens = set(re.findall(r"[a-z0-9]+", text.lower()))
            keyword_score = len(q_tokens & d_tokens) / max(1, math.sqrt(len(q_tokens)))
            metadata_boost = 0.0
            if meta.get("document_type") == "rfi" and {"rfi", "rfis", "unresolved", "open"} & q_tokens:
                metadata_boost += 0.45
            if meta.get("document_type") == "change_orders" and {"change", "order", "revision", "impact"} & q_tokens:
                metadata_boost += 0.45
            score = vector_score + 0.18 * keyword_score + metadata_boost
            results.append({"text": text, "metadata": meta, "score": score})
        return sorted(results, key=lambda item: item["score"], reverse=True)[:top_k]


def rebuild_index() -> dict[str, Any]:
    return LocalVectorStore().build()
