from __future__ import annotations

import importlib

def answer_drawing_question(project_id: str, question: str, model: str) -> dict:
    import src.agents.retrieval_agent as retrieval_agent_module

    retrieval_agent_module = importlib.reload(retrieval_agent_module)
    scoped = f"Focus on drawings, panel labels, circuits, equipment, rooms, conduit paths, and drawing notes. {question}"
    return retrieval_agent_module.answer_project_question(project_id, scoped, model)
