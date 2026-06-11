from __future__ import annotations

import json
import re

from src.services.file_db_service import save_chat
from src.services.vector_store_service import LocalVectorStore


def answer_project_question(project_id: str, question: str, model: str, technician_mode: bool = False) -> dict:
    store = LocalVectorStore()
    docs = store.search(question, project_id, top_k=5)
    usable = [doc for doc in docs if doc["score"] > 0.08]
    if not usable:
        answer = "I could not find that in the project documents."
        save_chat(project_id, question, answer, [])
        return {"answer": answer, "sources": [], "context": []}
    context = "\n\n".join(
        f"Source: {doc['metadata']['source_file']} page {doc['metadata'].get('page_number') or 'n/a'}\n{doc['text'][:700]}"
        for doc in usable
    )
    style = "Use simple field technician wording and give practical on-site instructions." if technician_mode else "Use a professional project-management style."
    prompt = f"""You are an electrical construction project copilot. Answer only from the context.
If the answer is not in the context, say: I could not find that in the project documents.
{style}

Question: {question}

Context:
{context}

Answer with concise bullets when useful and cite source filenames inline."""
    used_llm = False
    if model == "offline":
        answer = _extractive_answer(question, usable, technician_mode)
    else:
        from src.services.ollama_service import OllamaService

        llm = OllamaService(model)
        answer = llm.generate(prompt)
        used_llm = not answer.startswith("Ollama request failed")
    sources = [
        {
            "source_file": doc["metadata"]["source_file"],
            "page_number": doc["metadata"].get("page_number"),
            "document_type": doc["metadata"].get("document_type"),
            "score": round(doc["score"], 3),
        }
        for doc in usable
    ]
    save_chat(project_id, question, answer, sources)
    return {"answer": answer, "sources": sources, "context": usable, "used_llm": used_llm}


def _extractive_answer(question: str, docs: list[dict], technician_mode: bool) -> str:
    if _looks_like_rfi_question(question):
        return _rfi_fallback_answer(docs)

    lines = []
    for doc in docs[:3]:
        text = _clean_snippet(doc["text"])
        snippet = text[:420] + ("..." if len(text) > 420 else "")
        source = doc["metadata"]["source_file"]
        lines.append(f"- {snippet} Source: {source}.")
    heading = "Field answer from project documents:" if technician_mode else "Answer from project documents:"
    return heading + "\n" + "\n".join(lines)


def _looks_like_rfi_question(question: str) -> bool:
    terms = {"rfi", "rfis", "unresolved", "open", "change order", "revision"}
    text = question.lower()
    return any(term in text for term in terms)


def _rfi_fallback_answer(docs: list[dict]) -> str:
    items = []
    for doc in docs:
        if doc["metadata"].get("document_type") != "rfi":
            continue
        try:
            parsed = json.loads(doc["text"])
        except json.JSONDecodeError:
            continue
        for item in parsed:
            status = item.get("status", "Unknown")
            answer = item.get("answer") or "No answer posted yet."
            items.append(f"- {item.get('id', 'RFI')}: {status}. {item.get('question', '')} Answer: {answer}")
    if items:
        return "RFI summary from project documents:\n" + "\n".join(items)
    return "I could not find RFI details in the project documents."


def _clean_snippet(text: str) -> str:
    text = re.sub(r"^\s{0,3}#{1,6}\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"\s+", " ", text).strip()
    return text
