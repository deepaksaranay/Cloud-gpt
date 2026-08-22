import csv
from pathlib import Path


def extract_csv(source_path: str | Path) -> list[dict]:
    """Read a CSV file into a list of row dicts (all values as strings)."""
    path = Path(source_path)
    if not path.is_file():
        raise FileNotFoundError(f"CSV source not found: {path}")

    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))
