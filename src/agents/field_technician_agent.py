from __future__ import annotations

import importlib

def answer_for_field(project_id: str, question: str, model: str) -> dict:
    import src.agents.retrieval_agent as retrieval_agent_module

    retrieval_agent_module = importlib.reload(retrieval_agent_module)
    result = retrieval_agent_module.answer_project_question(project_id, question, model, technician_mode=True)
    result["answer"] = "Technician mode:\n" + result["answer"]
    return result
