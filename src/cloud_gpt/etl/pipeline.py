import argparse
from pathlib import Path

from cloud_gpt.etl.extract import extract_csv
from cloud_gpt.etl.load import load_to_sqlite
from cloud_gpt.etl.transform import transform


def run_pipeline(source_path: str | Path, db_path: str | Path, table: str = "orders") -> dict:
    """Extract orders from a CSV file, transform/validate them, and load into SQLite."""
    raw_rows = extract_csv(source_path)
    result = transform(raw_rows)
    loaded = load_to_sqlite(result.records, db_path, table=table)

    return {
        "extracted": len(raw_rows),
        "loaded": loaded,
        "rejected": len(result.rejected),
        "rejections": result.rejected,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the orders ETL pipeline.")
    parser.add_argument("source_csv", help="Path to the input CSV file")
    parser.add_argument("db_path", help="Path to the output SQLite database")
    parser.add_argument("--table", default="orders", help="Target table name (default: orders)")
    args = parser.parse_args()

    summary = run_pipeline(args.source_csv, args.db_path, table=args.table)
    print(f"Extracted {summary['extracted']} rows, loaded {summary['loaded']}, rejected {summary['rejected']}")
    for row, reason in summary["rejections"]:
        print(f"  rejected {row.get('order_id', '?')}: {reason}")


if __name__ == "__main__":
    main()
