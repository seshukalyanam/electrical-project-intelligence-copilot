from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.generate_sample_dataset import main as generate_dataset
from src.services.estimate_service import generate_estimate


def test_estimator_generates_positive_total():
    generate_dataset()
    df, summary, path = generate_estimate("food_mart")
    assert not df.empty
    assert summary["total_cost"] > 0
    assert path.exists()
