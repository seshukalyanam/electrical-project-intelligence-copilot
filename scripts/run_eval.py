from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.agents.retrieval_agent import answer_project_question
from src.services.estimate_service import generate_estimate
from src.utils.config import LOCAL_DB_DIR
from src.utils.helpers import utc_stamp


def main() -> None:
    questions = json.loads((ROOT / "tests" / "sample_questions.json").read_text(encoding="utf-8"))
    rows = []
    for item in questions:
        result = answer_project_question(item["project_id"], item["question"], "offline")
        answer = result["answer"].lower()
        expected = item["expected_contains"].lower()
        rows.append({
            "project_id": item["project_id"],
            "question": item["question"],
            "expected_contains": item["expected_contains"],
            "passed": expected in answer or any(expected in doc["text"].lower() for doc in result.get("context", [])),
            "source_count": len(result["sources"]),
        })
    for project_id in ["school", "hospital", "food_mart"]:
        df, summary, _ = generate_estimate(project_id)
        rows.append({"project_id": project_id, "question": "estimator_total_positive", "expected_contains": "total", "passed": summary["total_cost"] > 0, "source_count": len(df)})
    out_dir = LOCAL_DB_DIR / "evaluation_results"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"eval_{utc_stamp()}.json"
    out.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    passed = sum(1 for row in rows if row["passed"])
    print(f"Evaluation passed {passed}/{len(rows)} checks. Results: {out}")


if __name__ == "__main__":
    main()
