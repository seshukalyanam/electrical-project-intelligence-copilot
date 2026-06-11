from __future__ import annotations

import requests

from src.utils import config

OLLAMA_HOST = config.OLLAMA_HOST
OLLAMA_TIMEOUT_SECONDS = getattr(config, "OLLAMA_TIMEOUT_SECONDS", 600)


class OllamaService:
    _models_cache: dict[str, list[str]] = {}

    def __init__(self, model: str, host: str = OLLAMA_HOST):
        self.model = model
        self.host = host.rstrip("/")

    def is_available(self) -> bool:
        try:
            response = requests.get(f"{self.host}/api/tags", timeout=2)
            return response.ok
        except requests.RequestException:
            return False

    def list_models(self) -> list[str]:
        if self.host in self._models_cache:
            return self._models_cache[self.host]
        try:
            response = requests.get(f"{self.host}/api/tags", timeout=2)
            response.raise_for_status()
            models = [item["name"] for item in response.json().get("models", []) if item.get("name")]
        except requests.RequestException:
            models = []
        self._models_cache[self.host] = models
        return models

    def generate(self, prompt: str) -> str:
        try:
            response = requests.post(
                f"{self.host}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.1, "num_predict": 350},
                },
                timeout=OLLAMA_TIMEOUT_SECONDS,
            )
            response.raise_for_status()
            return response.json().get("response", "").strip()
        except Exception as exc:
            return f"Ollama request failed for model '{self.model}'. Confirm Ollama is running and the model is pulled. Details: {exc}"
