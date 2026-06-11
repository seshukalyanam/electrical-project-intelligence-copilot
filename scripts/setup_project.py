from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.utils.config import DATA_DIR, DATA_SUBFOLDERS, LOCAL_DB_DIR, LOCAL_DB_SUBFOLDERS, PROJECTS, VECTOR_STORE_DIR


def main() -> None:
    for project_id in PROJECTS:
        for folder in DATA_SUBFOLDERS:
            (DATA_DIR / project_id / folder).mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "shared").mkdir(parents=True, exist_ok=True)
    for folder in LOCAL_DB_SUBFOLDERS:
        (LOCAL_DB_DIR / folder).mkdir(parents=True, exist_ok=True)
    VECTOR_STORE_DIR.mkdir(parents=True, exist_ok=True)
    print("Project folders are ready.")


if __name__ == "__main__":
    main()
