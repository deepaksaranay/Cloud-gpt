import sqlite3
from pathlib import Path

from cloud_gpt.etl.pipeline import run_pipeline

SAMPLE_CSV = Path(__file__).resolve().parents[2] / "data" / "sales_sample.csv"


def test_pipeline_end_to_end(tmp_path):
    db_path = tmp_path / "orders.db"

    summary = run_pipeline(SAMPLE_CSV, db_path)

    assert summary["extracted"] == 7
    assert summary["loaded"] == 3
    assert summary["rejected"] == 4

    with sqlite3.connect(db_path) as conn:
        order_ids = {row[0] for row in conn.execute("SELECT order_id FROM orders")}
    assert order_ids == {"1001", "1002", "1006"}


def test_pipeline_rerun_is_idempotent(tmp_path):
    db_path = tmp_path / "orders.db"

    run_pipeline(SAMPLE_CSV, db_path)
    summary = run_pipeline(SAMPLE_CSV, db_path)

    with sqlite3.connect(db_path) as conn:
        count = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
    assert count == 3
    assert summary["loaded"] == 3
