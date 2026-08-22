import sqlite3

from cloud_gpt.etl.load import load_to_sqlite

RECORD = {
    "order_id": "1001",
    "customer_name": "Alice Nguyen",
    "email": "alice@example.com",
    "product": "Widget",
    "quantity": 3,
    "unit_price": 9.99,
    "total_price": 29.97,
    "order_date": "2024-01-15",
}


def test_load_creates_table_and_inserts_rows(tmp_path):
    db_path = tmp_path / "orders.db"

    loaded = load_to_sqlite([RECORD], db_path)

    assert loaded == 1
    with sqlite3.connect(db_path) as conn:
        rows = conn.execute("SELECT order_id, customer_name, total_price FROM orders").fetchall()
    assert rows == [("1001", "Alice Nguyen", 29.97)]


def test_load_is_idempotent_on_rerun(tmp_path):
    db_path = tmp_path / "orders.db"

    load_to_sqlite([RECORD], db_path)
    updated = {**RECORD, "customer_name": "Alice N."}
    load_to_sqlite([updated], db_path)

    with sqlite3.connect(db_path) as conn:
        rows = conn.execute("SELECT order_id, customer_name FROM orders").fetchall()
    assert rows == [("1001", "Alice N.")]
