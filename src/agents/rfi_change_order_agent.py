from __future__ import annotations

import importlib

def answer_rfi_change_order(project_id: str, question: str, model: str) -> dict:
    import src.agents.retrieval_agent as retrieval_agent_module

    retrieval_agent_module = importlib.reload(retrieval_agent_module)
    scoped = f"Focus on RFIs, unresolved issues, change orders, schedule impact, and cost impact. {question}"
    return retrieval_agent_module.answer_project_question(project_id, scoped, model)
