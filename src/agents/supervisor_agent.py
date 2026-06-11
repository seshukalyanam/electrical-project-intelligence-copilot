from __future__ import annotations

import importlib

try:
    from langgraph.graph import END, StateGraph
except Exception:
    END = None
    StateGraph = None

def route_question(question: str, mode: str) -> str:
    text = f"{mode} {question}".lower()
    if "estimate" in text or "takeoff" in text or "cost" in text:
        return "estimator"
    if "rfi" in text or "change order" in text or "revision" in text or "unresolved" in text:
        return "rfi"
    if "drawing" in text or "layout" in text or "conduit" in text or "circuit" in text:
        return "drawing"
    if "technician" in text or mode.lower().startswith("field"):
        return "field"
    return "retrieval"


def run_supervisor(project_id: str, question: str, mode: str, model: str) -> dict:
    route = route_question(question, mode)
    if route == "estimator":
        from src.agents.estimator_agent import run_estimator

        estimate = run_estimator(project_id)
        return {"route": route, "answer": f"Generated estimate with total cost ${estimate['summary']['total_cost']:,.2f}.", "estimate": estimate, "sources": [], "used_llm": False}
    if route == "rfi":
        from src.agents.rfi_change_order_agent import answer_rfi_change_order

        return {"route": route, **answer_rfi_change_order(project_id, question, model)}
    if route == "drawing":
        from src.agents.drawing_agent import answer_drawing_question

        return {"route": route, **answer_drawing_question(project_id, question, model)}
    if route == "field":
        from src.agents.field_technician_agent import answer_for_field

        return {"route": route, **answer_for_field(project_id, question, model)}
    import src.agents.retrieval_agent as retrieval_agent_module

    retrieval_agent_module = importlib.reload(retrieval_agent_module)
    return {"route": route, **retrieval_agent_module.answer_project_question(project_id, question, model)}


def build_langgraph():
    if StateGraph is None:
        return None
    graph = StateGraph(dict)
    graph.add_node("supervisor", lambda state: state)
    graph.set_entry_point("supervisor")
    graph.add_edge("supervisor", END)
    return graph.compile()
