from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.services.vector_store_service import rebuild_index


def main() -> None:
    result = rebuild_index()
    print(f"Built local vector index: {result}")


if __name__ == "__main__":
    main()
