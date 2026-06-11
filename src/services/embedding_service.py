from __future__ import annotations

import hashlib
from typing import Sequence

import numpy as np

from src.utils.config import EMBEDDING_MODEL, USE_SENTENCE_TRANSFORMERS


class EmbeddingService:
    def __init__(self, model_name: str = EMBEDDING_MODEL):
        self.model_name = model_name
        self._model = None

    def _load_model(self):
        if not USE_SENTENCE_TRANSFORMERS:
            raise RuntimeError("Sentence Transformers disabled; using local hash embeddings.")
        if self._model is None:
            from sentence_transformers import SentenceTransformer

            self._model = SentenceTransformer(self.model_name)
        return self._model

    def embed(self, texts: Sequence[str]) -> np.ndarray:
        try:
            model = self._load_model()
            vectors = model.encode(list(texts), normalize_embeddings=True, show_progress_bar=False)
            return np.asarray(vectors, dtype=np.float32)
        except Exception:
            return np.asarray([self._hash_embedding(text) for text in texts], dtype=np.float32)

    @staticmethod
    def _hash_embedding(text: str, dims: int = 384) -> np.ndarray:
        vec = np.zeros(dims, dtype=np.float32)
        for token in text.lower().split():
            digest = hashlib.md5(token.encode("utf-8")).digest()
            idx = int.from_bytes(digest[:4], "little") % dims
            vec[idx] += 1.0
        norm = np.linalg.norm(vec)
        return vec / norm if norm else vec
