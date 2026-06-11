from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.services.document_loader import load_all_documents


def main() -> None:
    chunks = load_all_documents()
    print(f"Loaded {len(chunks)} document chunks.")
    by_project = {}
    for chunk in chunks:
        by_project[chunk.metadata["project_id"]] = by_project.get(chunk.metadata["project_id"], 0) + 1
    print(by_project)


if __name__ == "__main__":
    main()
