from __future__ import annotations

from src.services.estimate_service import generate_estimate


def run_estimator(project_id: str, category_filter: str | None = None) -> dict:
    df, summary, path = generate_estimate(project_id, category_filter)
    return {"table": df, "summary": summary, "output_path": path}
